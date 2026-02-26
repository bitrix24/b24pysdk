from dataclasses import is_dataclass
from datetime import datetime
from typing import Text, Type, TypeVar

import pytest

from b24pysdk.api.responses import BitrixTimeResponse
from b24pysdk.utils.types import JSONDict
from tests.constants import PYTHON_VERSION

ResponseT = TypeVar("ResponseT")


def assert_frozen_instance(cls: Type[ResponseT], sample_data: JSONDict, field: Text):
    obj = cls.from_dict(sample_data)
    with pytest.raises(AttributeError):
        setattr(obj, field, None)


def assert_equality_disabled(cls: Type[ResponseT], sample_data: JSONDict):
    obj1 = cls.from_dict(sample_data)
    obj2 = cls.from_dict(sample_data)
    assert obj1 is not obj2
    assert obj1 != obj2


def assert_is_dataclass(cls: Type[ResponseT]):
    assert is_dataclass(cls)


def assert_slots(cls: Type[ResponseT]):
    if PYTHON_VERSION >= (3, 10):
        assert hasattr(cls, "__slots__")


def verify_time(time_obj: BitrixTimeResponse, time_data: JSONDict):
    assert time_obj.start == time_data["start"]
    assert time_obj.finish == time_data["finish"]
    assert time_obj.duration == time_data["duration"]
    assert time_obj.processing == time_data["processing"]
    assert time_obj.date_start == datetime.fromisoformat(time_data["date_start"])
    assert time_obj.date_finish == datetime.fromisoformat(time_data["date_finish"])
