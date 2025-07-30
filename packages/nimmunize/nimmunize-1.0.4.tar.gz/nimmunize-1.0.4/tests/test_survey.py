import pandas as pd
import datetime as _dt
from nimmunize.survey import load, audit, list_missed, list_complete, metrics

SAMPLE = pd.DataFrame(
    {"dob": ["2024-01-01", "2024-01-01"], "bcg": ["2024-01-01", None]}
)


def test_load_and_parse_dates(tmp_path):
    path = tmp_path / "sample.csv"
    SAMPLE.to_csv(path, index=False)
    df = load(path)
    assert isinstance(df.loc[0, "dob"], _dt.date)
    assert df.loc[1, "bcg"] is None


def test_audit_appends_columns():
    df = load(SAMPLE)
    audited = audit(df, as_of="2024-01-02")
    assert "missed_bcg" in audited.columns and "bcg" in audited.columns


def test_list_missed_and_complete():
    df = audit(load(SAMPLE), as_of="2024-01-02")
    missed = list_missed(df)
    complete = list_complete(df)
    assert len(missed) == 1 and len(complete) == 1


def test_metrics_output():
    m = metrics(audit(load(SAMPLE), as_of="2024-01-02"))
    assert "coverage_%" in m and "FIC_%" in m
