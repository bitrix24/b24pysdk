import datetime
import typing
import zoneinfo

from dateutil.parser import parse as _parse_dt

from . import types as _types

__all__ = [
    "bool_from_bitrix",
    "bool_to_bitrix",
    "date_from_bitrix",
    "date_to_bitrix",
    "datetime_from_bitrix",
    "datetime_to_bitrix",
    "dict_from_bitrix",
    "dict_to_bitrix",
    "float_from_bitrix",
    "float_to_bitrix",
    "int_from_bitrix",
    "int_to_bitrix",
    "text_from_bitrix",
    "text_to_bitrix",
    "time_from_bitrix",
    "time_to_bitrix",
    "timezone_from_bitrix",
    "timezone_to_bitrix",
]


@typing.overload
def bool_from_bitrix(value: typing.Union[bool, int, typing.Annotated[typing.Text, _types.B24BoolStrictLiteral]], /, *, is_required: typing.Literal[True]) -> bool: ...

@typing.overload
def bool_from_bitrix(value: typing.Optional[typing.Union[bool, int, typing.Annotated[typing.Text, _types.B24BoolLiteral]]], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[bool]: ...

def bool_from_bitrix(value: typing.Optional[typing.Union[bool, int, typing.Annotated[typing.Text, _types.B24BoolLiteral]]], /, *, is_required: bool = False) -> typing.Optional[bool]:
    """
    Convert a Bitrix24 boolean value to Python ``bool``.

    Args:
        value: Bitrix24 boolean value.
        is_required: Whether default and empty values should be treated as an
            error.

    Returns:
        Python ``bool`` instance. Returns ``None`` when ``is_required`` is
        False and the input value is ``D`` or ``None``.

    Raises:
        ValueError: If the value cannot be converted to ``bool``.
    """

    if value is True:
        return True

    if value is False:
        return False

    if value in {1, "1", "Y"}:
        return True

    if value in {0, "0", "N"}:
        return False

    if not is_required and value in {None, "D"}:
        return None

    raise ValueError(f"Cannot convert Bitrix24 value to bool: {value!r}")

@typing.overload
def bool_to_bitrix(value: bool, /, *, is_required: typing.Literal[True], serialize_as: typing.Type[bool]) -> bool: ...

@typing.overload
def bool_to_bitrix(value: typing.Optional[bool], /, *, is_required: typing.Literal[False] = False, serialize_as: typing.Type[bool]) -> typing.Optional[bool]: ...

@typing.overload
def bool_to_bitrix(value: bool, /, *, is_required: typing.Literal[True], serialize_as: typing.Type[int]) -> typing.Literal[0, 1]: ...

@typing.overload
def bool_to_bitrix(value: typing.Optional[bool], /, *, is_required: typing.Literal[False] = False, serialize_as: typing.Type[int]) -> typing.Optional[typing.Literal[0, 1]]: ...

@typing.overload
def bool_to_bitrix(value: bool, /, *, is_required: typing.Literal[True], serialize_as: typing.Type[typing.Text] = str) -> _types.B24BoolStrictLiteral: ...

@typing.overload
def bool_to_bitrix(value: typing.Optional[bool], /, *, is_required: typing.Literal[False] = False, serialize_as: typing.Type[typing.Text] = str) -> _types.B24BoolLiteral: ...

def bool_to_bitrix(
        value: typing.Optional[bool],
        /,
        *,
        is_required: bool = False,
        serialize_as: typing.Type[typing.Union[bool, int, typing.Text]] = str,
) -> typing.Optional[typing.Union[bool, int, typing.Text]]:
    """
    Convert a Python ``bool`` value to Bitrix24 boolean value.

    Args:
        value: Python boolean value.
        is_required: Whether ``None`` should be treated as an error.
        serialize_as: Outgoing representation type. Use ``str`` for ``Y``/``N``
            and optional ``D``, ``int`` for ``1``/``0``, or ``bool`` for native
            booleans used by API v3.

    Returns:
        Bitrix24 boolean value in the requested representation. An optional
        ``None`` is serialized as ``D`` for the string format and as ``None``
        for the integer and boolean formats.

    Raises:
        TypeError: If ``serialize_as`` is not ``str``, ``int``, or ``bool``.
        ValueError: If the value is required but ``None`` or cannot be
            converted to a Bitrix24 boolean value.
    """

    if serialize_as not in (bool, int, str):
        raise TypeError("serialize_as must be bool, int, or str.")

    if value is True:
        if serialize_as is bool:
            return True

        return 1 if serialize_as is int else "Y"

    if value is False:
        if serialize_as is bool:
            return False

        return 0 if serialize_as is int else "N"

    if value is None and not is_required:
        return "D" if serialize_as is str else None

    raise ValueError(f"Cannot convert Python value to Bitrix24 bool: {value!r}")

@typing.overload
def datetime_from_bitrix(value: typing.Text, /, *, is_required: typing.Literal[True]) -> datetime.datetime: ...

@typing.overload
def datetime_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[datetime.datetime]: ...

def datetime_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: bool = False) -> typing.Optional[datetime.datetime]:
    """
    Convert a Bitrix24 datetime value to Python ``datetime``.

    Args:
        value: Bitrix24 datetime value.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``datetime`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``datetime``.
    """

    if not value:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to datetime: {value!r}")

    if isinstance(value, str):
        try:
            return datetime.datetime.fromisoformat(value)
        except ValueError:
            return _parse_dt(value, dayfirst=True)

    raise ValueError(f"Cannot convert Bitrix24 value to datetime: {value!r}")

@typing.overload
def date_from_bitrix(value: typing.Text, /, *, is_required: typing.Literal[True]) -> datetime.date: ...

@typing.overload
def date_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[datetime.date]: ...

def date_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: bool = False) -> typing.Optional[datetime.date]:
    """
    Convert a Bitrix24 date value to Python ``date``.

    Args:
        value: Bitrix24 date value.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``date`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``date``.
    """

    if not value:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to date: {value!r}")

    if isinstance(value, str):
        try:
            return datetime.date.fromisoformat(value[:10])
        except ValueError:
            return _parse_dt(value, dayfirst=True).date()

    raise ValueError(f"Cannot convert Bitrix24 value to date: {value!r}")

@typing.overload
def date_to_bitrix(value: datetime.date, /, *, is_required: typing.Literal[True]) -> typing.Text: ...

@typing.overload
def date_to_bitrix(value: typing.Optional[datetime.date], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[typing.Text]: ...

def date_to_bitrix(value: typing.Optional[datetime.date], /, *, is_required: bool = False) -> typing.Optional[typing.Text]:
    """
    Convert a Python ``date`` value to Bitrix24 date value.

    Args:
        value: Python date value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 date value. Returns ``None`` when ``is_required`` is False
        and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 date.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 date: {value!r}")

    if isinstance(value, datetime.datetime):
        return value.date().isoformat()

    if isinstance(value, datetime.date):
        return value.isoformat()

    raise ValueError(f"Cannot convert Python value to Bitrix24 date: {value!r}")

@typing.overload
def datetime_to_bitrix(value: datetime.datetime, /, *, is_required: typing.Literal[True]) -> typing.Text: ...

@typing.overload
def datetime_to_bitrix(value: typing.Optional[datetime.datetime], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[typing.Text]: ...

def datetime_to_bitrix(value: typing.Optional[datetime.datetime], /, *, is_required: bool = False) -> typing.Optional[typing.Text]:
    """
    Convert a Python ``datetime`` value to Bitrix24 datetime value.

    Args:
        value: Python datetime value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 datetime value with seconds precision. Returns ``None`` when
        ``is_required`` is False and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 datetime.
    """

    if not value:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 datetime: {value!r}")

    if isinstance(value, datetime.datetime):
        return value.isoformat(timespec="seconds")

    raise ValueError(f"Cannot convert Python value to Bitrix24 datetime: {value!r}")

@typing.overload
def dict_from_bitrix(value: _types.JSONDict, /, *, is_required: typing.Literal[True]) -> _types.JSONDict: ...

@typing.overload
def dict_from_bitrix(value: typing.Optional[_types.JSONDict], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[_types.JSONDict]: ...

def dict_from_bitrix(value: typing.Optional[_types.JSONDict], /, *, is_required: bool = False) -> typing.Optional[_types.JSONDict]:
    """
    Convert a Bitrix24 dictionary value to Python ``dict``.

    Args:
        value: Bitrix24 dictionary value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        The original Python ``dict`` instance, or ``None`` when
        ``is_required`` is False and the input value is ``None``. Preserving
        identity allows an object field mapping to be changed in place and
        then explicitly persisted through ``save(update_fields=[...])``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to ``dict``.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to dict: {value!r}")

    if isinstance(value, dict):
        return value

    raise ValueError(f"Cannot convert Bitrix24 value to dict: {value!r}")

@typing.overload
def dict_to_bitrix(value: _types.JSONDict, /, *, is_required: typing.Literal[True]) -> _types.JSONDict: ...

@typing.overload
def dict_to_bitrix(value: typing.Optional[_types.JSONDict], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[_types.JSONDict]: ...

def dict_to_bitrix(value: typing.Optional[_types.JSONDict], /, *, is_required: bool = False) -> typing.Optional[_types.JSONDict]:
    """
    Convert a Python ``dict`` value to Bitrix24 dictionary value.

    Args:
        value: Python dictionary value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 dictionary value. Returns ``None`` when ``is_required`` is
        False and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 dictionary value.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 dict: {value!r}")

    if isinstance(value, dict):
        return dict(value)

    raise ValueError(f"Cannot convert Python value to Bitrix24 dict: {value!r}")

@typing.overload
def float_from_bitrix(value: typing.Union[float, typing.Text], /, *, is_required: typing.Literal[True]) -> float: ...

@typing.overload
def float_from_bitrix(value: typing.Optional[typing.Union[int, float, typing.Text]], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[float]: ...

def float_from_bitrix(value: typing.Optional[typing.Union[int, float, typing.Text]], /, *, is_required: bool = False) -> typing.Optional[float]:
    """
    Convert a Bitrix24 float value to Python ``float``.

    Args:
        value: Bitrix24 float value.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``float`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``float``.
    """

    if value is None or value == "":
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to float: {value!r}")

    if isinstance(value, bool):
        raise TypeError(f"Cannot convert Bitrix24 value to float: {value!r}")

    if isinstance(value, float):
        return value

    if isinstance(value, (int, str)):
        try:
            return float(value)
        except ValueError as error:
            raise ValueError(f"Cannot convert Bitrix24 value to float: {value!r}") from error

    raise ValueError(f"Cannot convert Bitrix24 value to float: {value!r}")

@typing.overload
def float_to_bitrix(value: float, /, *, is_required: typing.Literal[True]) -> float: ...

@typing.overload
def float_to_bitrix(value: typing.Optional[typing.Union[int, float]], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[float]: ...

def float_to_bitrix(value: typing.Optional[typing.Union[int, float]], /, *, is_required: bool = False) -> typing.Optional[float]:
    """
    Convert a Python ``float`` value to Bitrix24 float value.

    Args:
        value: Python float value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 float value. Returns ``None`` when ``is_required`` is False
        and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 float.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 float: {value!r}")

    if isinstance(value, bool):
        raise TypeError(f"Cannot convert Python value to Bitrix24 float: {value!r}")

    if isinstance(value, float):
        return value

    if isinstance(value, int):
        return float(value)

    raise ValueError(f"Cannot convert Python value to Bitrix24 float: {value!r}")

@typing.overload
def int_from_bitrix(value: typing.Union[int, typing.Text], /, *, is_required: typing.Literal[True]) -> int: ...

@typing.overload
def int_from_bitrix(value: typing.Optional[typing.Union[int, typing.Text]], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[int]: ...

def int_from_bitrix(value: typing.Optional[typing.Union[int, typing.Text]], /, *, is_required: bool = False) -> typing.Optional[int]:
    """
    Convert a Bitrix24 integer value to Python ``int``.

    Args:
        value: Bitrix24 integer value.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``int`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``int``.
    """

    if value is None or value == "":
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to int: {value!r}")

    if isinstance(value, bool):
        raise TypeError(f"Cannot convert Bitrix24 value to int: {value!r}")

    if isinstance(value, int):
        return value

    if isinstance(value, str):
        try:
            return int(value)
        except ValueError as error:
            raise ValueError(f"Cannot convert Bitrix24 value to int: {value!r}") from error

    raise ValueError(f"Cannot convert Bitrix24 value to int: {value!r}")

@typing.overload
def int_to_bitrix(value: int, /, *, is_required: typing.Literal[True]) -> int: ...

@typing.overload
def int_to_bitrix(value: typing.Optional[int], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[int]: ...

def int_to_bitrix(value: typing.Optional[int], /, *, is_required: bool = False) -> typing.Optional[int]:
    """
    Convert a Python ``int`` value to Bitrix24 integer value.

    Args:
        value: Python integer value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 integer value. Returns ``None`` when ``is_required`` is False
        and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 integer.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 int: {value!r}")

    if isinstance(value, bool):
        raise TypeError(f"Cannot convert Python value to Bitrix24 int: {value!r}")

    if isinstance(value, int):
        return value

    raise ValueError(f"Cannot convert Python value to Bitrix24 int: {value!r}")

@typing.overload
def text_from_bitrix(value: typing.Text, /, *, is_required: typing.Literal[True]) -> typing.Text: ...

@typing.overload
def text_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[typing.Text]: ...

def text_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: bool = False) -> typing.Optional[typing.Text]:
    """
    Convert a Bitrix24 text value to Python ``str``.

    Args:
        value: Bitrix24 text value.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``str`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``str``.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to text: {value!r}")

    if isinstance(value, str):
        return value

    raise ValueError(f"Cannot convert Bitrix24 value to text: {value!r}")

@typing.overload
def text_to_bitrix(value: typing.Text, /, *, is_required: typing.Literal[True]) -> typing.Text: ...

@typing.overload
def text_to_bitrix(value: typing.Optional[typing.Text], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[typing.Text]: ...

def text_to_bitrix(value: typing.Optional[typing.Text], /, *, is_required: bool = False) -> typing.Optional[typing.Text]:
    """
    Convert a Python ``str`` value to Bitrix24 text value.

    Args:
        value: Python text value.
        is_required: Whether ``None`` or an empty string should be treated as an
            error.

    Returns:
        Bitrix24 text value. Returns ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to Bitrix24 text.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 text: {value!r}")

    if isinstance(value, str):
        return value

    raise ValueError(f"Cannot convert Python value to Bitrix24 text: {value!r}")

@typing.overload
def time_from_bitrix(value: typing.Text, /, *, is_required: typing.Literal[True]) -> datetime.time: ...

@typing.overload
def time_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[datetime.time]: ...

def time_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: bool = False) -> typing.Optional[datetime.time]:
    """
    Convert a Bitrix24 time value to Python ``time``.

    Args:
        value: Bitrix24 time value.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``time`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``time``.
    """

    if not value:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to time: {value!r}")

    if isinstance(value, str):
        try:
            return datetime.time.fromisoformat(value)
        except ValueError:
            return _parse_dt(value, dayfirst=True).time()

    raise ValueError(f"Cannot convert Bitrix24 value to time: {value!r}")

@typing.overload
def time_to_bitrix(value: datetime.time, /, *, is_required: typing.Literal[True]) -> typing.Text: ...

@typing.overload
def time_to_bitrix(value: typing.Optional[datetime.time], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[typing.Text]: ...

def time_to_bitrix(value: typing.Optional[datetime.time], /, *, is_required: bool = False) -> typing.Optional[typing.Text]:
    """
    Convert a Python ``time`` value to Bitrix24 time value.

    Args:
        value: Python time value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 time value with seconds precision. Returns ``None`` when
        ``is_required`` is False and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 time.
    """

    if value is None:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 time: {value!r}")

    if isinstance(value, datetime.time):
        return value.isoformat(timespec="minutes")

    raise ValueError(f"Cannot convert Python value to Bitrix24 time: {value!r}")

@typing.overload
def timezone_from_bitrix(value: typing.Text, /, *, is_required: typing.Literal[True]) -> zoneinfo.ZoneInfo: ...

@typing.overload
def timezone_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[zoneinfo.ZoneInfo]: ...

def timezone_from_bitrix(value: typing.Optional[typing.Text], /, *, is_required: bool = False) -> typing.Optional[zoneinfo.ZoneInfo]:
    """
    Convert a Bitrix24 timezone value to Python ``ZoneInfo``.

    Args:
        value: Bitrix24 timezone name.
        is_required: Whether empty values should be treated as an error.

    Returns:
        Python ``ZoneInfo`` instance, or ``None`` when ``is_required`` is False
        and the input value is empty.

    Raises:
        ValueError: If the value is required but empty, or cannot be converted
            to ``ZoneInfo``.
    """

    if not value:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Bitrix24 value to timezone: {value!r}")

    if isinstance(value, str):
        return zoneinfo.ZoneInfo(value)

    raise ValueError(f"Cannot convert Bitrix24 value to timezone: {value!r}")

@typing.overload
def timezone_to_bitrix(value: zoneinfo.ZoneInfo, /, *, is_required: typing.Literal[True]) -> typing.Text: ...

@typing.overload
def timezone_to_bitrix(value: typing.Optional[zoneinfo.ZoneInfo], /, *, is_required: typing.Literal[False] = False) -> typing.Optional[typing.Text]: ...

def timezone_to_bitrix(value: typing.Optional[zoneinfo.ZoneInfo], /, *, is_required: bool = False) -> typing.Optional[typing.Text]:
    """
    Convert a Python ``ZoneInfo`` value to Bitrix24 timezone value.

    Args:
        value: Python timezone value.
        is_required: Whether ``None`` should be treated as an error.

    Returns:
        Bitrix24 timezone name. Returns ``None`` when ``is_required`` is False
        and the input value is ``None``.

    Raises:
        ValueError: If the value is required but ``None``, or cannot be
            converted to Bitrix24 timezone.
    """

    if not value:
        if not is_required:
            return None

        raise ValueError(f"Cannot convert empty Python value to Bitrix24 timezone: {value!r}")

    if isinstance(value, zoneinfo.ZoneInfo):
        return value.key

    raise ValueError(f"Cannot convert Python value to Bitrix24 timezone: {value!r}")
