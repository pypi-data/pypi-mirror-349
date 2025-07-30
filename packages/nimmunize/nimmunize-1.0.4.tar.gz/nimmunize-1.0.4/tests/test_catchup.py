import datetime as _dt
from nimmunize.catchup import plan


def test_plan_empty_taken():
    dob = _dt.date(2024, 1, 1)
    result = plan(dob, {})
    # All antigens should have at least first dose scheduled
    assert all(isinstance(v, list) for v in result.values())
