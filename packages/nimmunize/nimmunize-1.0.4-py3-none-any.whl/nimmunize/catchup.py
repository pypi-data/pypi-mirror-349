"""
Catch‑up planner: rebuild safe schedule for children with missing immunisations.
Implements WHO catch‑up algorithm for routine vaccines.
"""

from __future__ import annotations
import datetime as _dt
from typing import Dict, List, Optional, Sequence

from .schedule import ANTIGENS, _doses, _nominal_due, _earliest_allowed


def plan(
    dob: _dt.date,
    taken: Dict[str, _dt.date | Sequence[_dt.date] | dict | None],
    *,
    as_of: Optional[_dt.date] = None,
) -> Dict[str, List[_dt.date]]:
    """
    For each antigen, return the full catch-up schedule for missing sequences.
    Implements WHO rules. Works even if doses are missing/skipped/out of order.
    """
    as_of = as_of or _dt.date.today()
    result: Dict[str, List[_dt.date]] = {}

    for antigen in ANTIGENS:
        doses_defs = _doses(antigen)
        # Normalize taken to a dict: sequence -> date
        taken_val = taken.get(antigen)
        if isinstance(taken_val, dict):
            given_by_seq = {int(seq): date for seq, date in taken_val.items()}
        else:
            # If it's a list or single date, map in order of dose sequence as in JSON
            shots = sorted(
                (
                    [taken_val]
                    if isinstance(taken_val, _dt.date)
                    else (list(taken_val) if taken_val else [])
                ),
                key=lambda d: d,
            )
            sequences = [d["sequence"] for d in doses_defs]
            given_by_seq = {
                seq: shots[i] for i, seq in enumerate(sequences) if i < len(shots)
            }

        prev_date: Optional[_dt.date] = None
        plan_dates: List[_dt.date] = []

        for dose_def in doses_defs:
            seq = dose_def["sequence"]
            # Skip if dose already recorded for this sequence
            if seq in given_by_seq:
                prev_date = given_by_seq[seq]
                continue

            # Compute nominal and earliest dates for missing dose
            nominal = _nominal_due(dob, dose_def)
            earliest = _earliest_allowed(dob, dose_def, prev_date)
            due = max(nominal, earliest)
            plan_dates.append(due)
            # Next dose should be calculated relative to this one (per WHO rules)
            prev_date = due

        result[antigen] = plan_dates

    return result
