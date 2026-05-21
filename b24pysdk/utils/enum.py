import enum as _enum
import typing

from .. import _constants

__all__ = [
    "IntEnum",
    "StrEnum",
]

_MIN_STR_WITH_ENCODING_ARGS: typing.Final[int] = 2
_MAX_STR_CONSTRUCTOR_ARGS: typing.Final[int] = 3


if _constants.PYTHON_VERSION >= (3, 11):
    IntEnum = _enum.IntEnum
else:
    class IntEnum(_enum.IntEnum):
        """"""

        def __str__(self) -> typing.Text:
            return str(self.value)


if _constants.PYTHON_VERSION >= (3, 11):
    StrEnum = _enum.StrEnum
else:
    class StrEnum(str, _enum.Enum):
        """"""

        def __new__(cls, *values: typing.Any) -> typing.Any:
            if len(values) > _MAX_STR_CONSTRUCTOR_ARGS:
                raise TypeError("too many arguments for str(): %r" % (values,))

            if len(values) == 1 and not isinstance(values[0], str):
                raise TypeError("%r is not a string" % (values[0],))

            if len(values) >= _MIN_STR_WITH_ENCODING_ARGS and not isinstance(values[1], str):
                raise TypeError("encoding must be a string, not %r" % (values[1],))

            if len(values) == _MAX_STR_CONSTRUCTOR_ARGS and not isinstance(values[2], str):
                raise TypeError("errors must be a string, not %r" % (values[2],))

            value = str(*values)
            member = str.__new__(cls, value)
            member._value_ = value

            return member

        def __repr__(self) -> typing.Text:
            return f"<{self.__class__.__name__}.{self.name}: {self.value!r}>"

        def __str__(self) -> typing.Text:
            return str(self.value)

        @staticmethod
        def _generate_next_value_(
                name: typing.Text,
                _start: int,
                _count: int,
                _last_values: typing.Sequence[typing.Any],
        ) -> typing.Text:
            return name.lower()
