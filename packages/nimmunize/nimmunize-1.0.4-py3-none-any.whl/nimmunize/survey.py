from __future__ import annotations
import pandas as pd
import datetime as _dt
from typing import Dict, List, Optional, Any

from .schedule import ANTIGENS, next_due as _next_due, overdue as _overdue

# -----------------------------------------------------------------------------
# DATE PARSING
# -----------------------------------------------------------------------------
_DOB_FMT_HINTS = ["%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%Y-%m", "%m/%Y"]


def _parse_date(val: Any) -> Optional[_dt.date]:
    """Smart-parse full or partial dates; YYYY-MM becomes day=15."""
    if pd.isna(val) or val is None:
        return None
    if isinstance(val, (_dt.date, pd.Timestamp)):
        return val.date() if isinstance(val, pd.Timestamp) else val  # type: ignore
    s = str(val).strip()
    for fmt in _DOB_FMT_HINTS:
        try:
            dt = _dt.datetime.strptime(s, fmt)
            if fmt in ("%Y-%m", "%m/%Y"):
                dt = dt.replace(day=15)
            return dt.date()
        except ValueError:
            continue
    raise ValueError(f"Un-parsable date: {val}")


# -----------------------------------------------------------------------------
# LOAD & NORMALISE
# -----------------------------------------------------------------------------
def load(
    path_or_df: str | pd.DataFrame,
    *,
    dob_col: str = "dob",
    vacc_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Read a CSV / Excel / DataFrame and normalise:
      - Date of birth to datetime.date
      - Vaccination columns coerced to datetime.date or None
    Stores the final `vacc_cols` in df.attrs['vacc_cols'].
    """
    if isinstance(path_or_df, pd.DataFrame):
        df = path_or_df.copy()
    else:
        df = (
            pd.read_excel(path_or_df)
            if str(path_or_df).lower().endswith((".xls", ".xlsx"))
            else pd.read_csv(path_or_df)
        )

    if dob_col not in df.columns:
        raise KeyError(f"Date-of-birth column '{dob_col}' not found")
    df[dob_col] = df[dob_col].apply(_parse_date)

    cols = vacc_cols or [c for c in df.columns if c.lower() in ANTIGENS]
    df.attrs["vacc_cols"] = cols
    for col in cols:
        df[col] = df[col].apply(_parse_date)
    return df


# -----------------------------------------------------------------------------
# AUDIT ROWS
# -----------------------------------------------------------------------------
def audit(
    df: pd.DataFrame, *, dob_col: str = "dob", as_of: _dt.date | str | None = None
) -> pd.DataFrame:
    """
    Vectorised audit → adds:
      - missed_<antigen>: bool
      - delay_<antigen>: Optional[int]
      - next_due_<antigen>: Optional[date] (the soonest pending dose)
      - all_due_<antigen>: List[date] (all pending doses)
    Only for antigens in df.attrs['vacc_cols'].
    """
    if isinstance(as_of, str):
        as_of = _parse_date(as_of)
    as_of = as_of or _dt.date.today()

    cols = df.attrs.get("vacc_cols", [])
    records: List[Dict[str, Any]] = []

    for _, row in df.iterrows():
        dob = row[dob_col]
        taken = {ag: row.get(ag) for ag in cols}
        od = _overdue(dob, taken, as_of=as_of)
        nd = _next_due(dob, taken, as_of=as_of)

        rec: Dict[str, Any] = {}
        # pull in both missed_ and delay_ keys from the overdue() result
        for key, value in od.items():
            antigen = key.split("_", 1)[1]
            if antigen in cols:
                rec[key] = value
        # Add next_due_<antigen> (first due), and all_due_<antigen> (full list)
        for antigen, dues in nd.items():
            if antigen in cols:
                # First due
                rec[f"next_due_{antigen}"] = (
                    dues[0]
                    if isinstance(dues, list) and dues
                    else (dues if dues else None)
                )
                # All due
                rec[f"all_due_{antigen}"] = (
                    dues if isinstance(dues, list) else ([dues] if dues else [])
                )
        records.append(rec)

    audited = pd.concat([df.reset_index(drop=True), pd.DataFrame(records)], axis=1)
    return audited


def metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    National-survey indicators:
      - coverage_%: {antigen: pct not missed}
      - FIC_%: percent with no missed doses
      - median_delay_days: {antigen: median delay}
    """
    # detect which columns we actually have
    miss_cols = [c for c in df.columns if c.startswith("missed_")]
    delay_cols = [c for c in df.columns if c.startswith("delay_")]

    # coverage: for each missed_<antigen>, invert and take mean
    coverage = {col.split("_", 1)[1]: 100 * (~df[col]).mean() for col in miss_cols}

    # fully immunised if none of the missed_ flags are True
    if miss_cols:
        fic = 100 * (~df[miss_cols]).all(axis=1).mean()
    else:
        fic = 0.0

    # median delays, only over non-null
    delays = {}
    for col in delay_cols:
        antigen = col.split("_", 1)[1]
        non_null = df[col].dropna()
        delays[antigen] = int(non_null.median()) if not non_null.empty else None

    return {
        "coverage_%": coverage,
        "FIC_%": fic,
        "median_delay_days": delays,
    }


# -----------------------------------------------------------------------------
# FILTERED ROWSETS
# -----------------------------------------------------------------------------
def list_missed(df: pd.DataFrame, antigen: Optional[str] = None) -> pd.DataFrame:
    """
    Return sub-DataFrame of children with any missed dose (or only a specific antigen).
    Dynamically detects all 'missed_*' columns in the audited DataFrame.
    """
    miss_cols = [col for col in df.columns if col.startswith("missed_")]
    if antigen:
        col = f"missed_{antigen}"
        miss_cols = [col] if col in df.columns else []
    if not miss_cols:
        return df.iloc[0:0]
    mask = pd.concat([df[c] for c in miss_cols], axis=1).any(axis=1)
    return df.loc[mask]


def list_complete(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return sub-DataFrame of children with no missed doses across all antigens loaded.
    Dynamically detects all 'missed_*' columns.
    """
    miss_cols = [col for col in df.columns if col.startswith("missed_")]
    if not miss_cols:
        return df.iloc[0:0]
    mask = ~pd.concat([df[c] for c in miss_cols], axis=1).any(axis=1)
    return df.loc[mask]


# -----------------------------------------------------------------------------
# COVERAGE BY ROUTE & DISEASE
# -----------------------------------------------------------------------------
# These maps are derived at import from schedule JSON
from .schedule import _SPEC as _SCH_SPEC

# build antigen → route lookup
_antigen_route: Dict[str, str] = {
    a["name"]: a["doses"][0].get("route", "unknown") for a in _SCH_SPEC["antigens"]
}

# build disease → antigens lookup
_disease_to_antigens: Dict[str, List[str]] = {}
for a in _SCH_SPEC["antigens"]:
    for dose in a["doses"]:
        for dis in dose.get("diseases_prevented", []):
            _disease_to_antigens.setdefault(dis, []).append(a["name"])


def route_coverage(df: pd.DataFrame) -> Dict[str, float]:
    """
    Percentage of children fully covered for antigens delivered by each route.
    """
    cols: List[str] = df.attrs.get("vacc_cols", [])
    # group series by route
    route_map: Dict[str, List[pd.Series]] = {}
    for ag in cols:
        route = _antigen_route.get(ag, "unknown")
        route_map.setdefault(route, []).append(~df[f"missed_{ag}"])

    return {
        route: 100 * pd.concat(series, axis=1).all(axis=1).mean()
        for route, series in route_map.items()
    }


def disease_coverage(df: pd.DataFrame) -> Dict[str, float]:
    """
    Percentage of children protected against each disease.
    (i.e., at least one complete antigen series that prevents that disease).
    """
    cols: List[str] = df.attrs.get("vacc_cols", [])
    miss_map = {ag: df[f"missed_{ag}"] for ag in cols}

    dis_cov: Dict[str, float] = {}
    for disease, ag_list in _disease_to_antigens.items():
        relevant = [~miss_map[ag] for ag in ag_list if ag in miss_map]
        if relevant:
            dis_cov[disease] = 100 * pd.concat(relevant, axis=1).any(axis=1).mean()
    return dis_cov


def diseases_at_risk(df: pd.DataFrame, *, threshold: float = 80.0) -> List[str]:
    """
    List diseases whose population protection is below *threshold* percent.
    """
    return [d for d, pct in disease_coverage(df).items() if pct < threshold]
