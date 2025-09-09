import datetime as dt

import pytest

from b24pysdk.bitrix_api.classes.bitrix_api_response_time import BitrixAPIResponseTime


def test_response_time_from_dict_and_to_dict():
    now = dt.datetime.now(dt.timezone.utc)
    later = now + dt.timedelta(seconds=1)

    payload = {
        "start": 0.1,
        "finish": 0.2,
        "duration": 0.1,
        "processing": 0.05,
        "date_start": now.isoformat(),
        "date_finish": later.isoformat(),
        "operating_reset_at": int(now.timestamp()),
        "operating": 0.08,
    }

    rt = BitrixAPIResponseTime.from_dict(payload)
    assert rt.duration == pytest.approx(0.1)
    assert rt.processing == pytest.approx(0.05)
    assert isinstance(rt.date_start, dt.datetime)
    assert isinstance(rt.date_finish, dt.datetime)

    # Round-trip via to_dict
    d = rt.to_dict()
    # dataclasses.asdict converts datetimes to isoformat? It preserves objects; check fields presence
    assert set(d.keys()) >= {"start", "finish", "duration", "processing", "date_start", "date_finish"}
