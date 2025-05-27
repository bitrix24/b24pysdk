from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Text,
    Tuple,
    Union,
)


JSONDict = Dict[Text, Any]
"""A dictionary containing response from the API or data to send to the API."""

JSONList = List[JSONDict]
"""A list containing response from the API or data to send to the API."""

B24APIResult = Union[JSONDict, JSONList, bool]
""""""

B24BatchRequestData = Tuple[Text, Optional[JSONDict]]
"""Tuple containing rest api method and parameters"""

B24BoolLiteral = Literal["Y", "N", "D"]
""""""


class B24BoolStr(str):
    """"""

    _ALLOWED_VALUES = frozenset({"Y", "N", "D"})

    def __new__(cls, value: B24BoolLiteral):
        if value not in cls._ALLOWED_VALUES:
            raise ValueError(f"Invalid B24BoolStr value: {value}. Must be one of {','.join(cls._ALLOWED_VALUES)}")
        return super().__new__(cls, value)

    def __bool__(self):
        return bool(B24Bool(self))

    def __repr__(self):
        return f"B24BoolStr('{self}')"


class B24Bool:
    """"""

    TRUE: B24BoolLiteral = "Y"
    FALSE: B24BoolLiteral = "N"
    DEFAULT: B24BoolLiteral = "D"

    _B24_VALUES = {
        True: TRUE,
        False: FALSE,
        None: DEFAULT,
    }

    __slots__ = ("_value",)

    def __init__(
            self,
            value: Optional[Union["B24Bool", B24BoolLiteral, B24BoolStr, bool]]
    ):
        self._value = self._normalize(value)

    def __bool__(self):
        return bool(self._value)

    def __str__(self):
        return self.to_b24()

    def __repr__(self):
        return f"B24Bool({self._value})"

    @classmethod
    def _normalize(
            cls,
            value: Optional[Union["B24Bool", B24BoolLiteral, B24BoolStr, bool]]
    ) -> Optional[bool]:
        """"""

        if isinstance(value, cls):
            return value._value

        elif value is True or value == cls.TRUE:
            return True

        elif value is False or value == cls.FALSE:
            return False

        elif value is None or value == cls.DEFAULT:
            return None

        else:
            raise ValueError(f"Invalid value for {cls.__name__}: {value}")

    @property
    def value(self) -> Optional[bool]:
        """"""
        return self._value

    def to_b24(self) -> B24BoolLiteral:
        """"""
        return self._B24_VALUES[self._value]

    @classmethod
    def from_b24(cls, value: B24BoolLiteral) -> "B24Bool":
        """"""
        return cls(value)


class RawStringParam:
    """Urlencoded string containing rest api method and its parameters."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __unicode__(self):
        return self.__str__()

    def __repr__(self):
        return f"<RawStringParam {self.value!r}>"
