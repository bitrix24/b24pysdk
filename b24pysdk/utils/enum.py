import enum as _enum
import typing

from .. import _constants

__all__ = [
    "IntEnum",
    "StrEnum",
]

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

        def __repr__(self) -> typing.Text:
            return f"<{self.__class__.__name__}.{self.name}: {self.value!r}>"

        def __str__(self) -> typing.Text:
            return str(self.value)
