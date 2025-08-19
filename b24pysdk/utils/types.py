import typing

JSONDict = typing.Dict[typing.Text, typing.Any]
"""A dictionary containing response from the API or data to send to the API."""

JSONList = typing.List[JSONDict]
"""A list containing response from the API or data to send to the API."""

Key = typing.Union[int, typing.Text]
""""""

Number = typing.Union[int, float]
""""""

DefaultTimeout = typing.Union[Number, typing.Tuple[Number, Number]]
""""""

Timeout = typing.Optional[DefaultTimeout]
""""""

B24APIResult = typing.Optional[typing.Union[JSONDict, JSONList, bool]]
""""""

B24BatchRequestData = typing.Tuple[typing.Text, typing.Optional[JSONDict]]
"""Tuple containing rest api method and its parameters"""

B24BoolLiteral = typing.Literal["Y", "N", "D"]
""""""


class B24BoolStr(str):
    """"""

    __slots__ = ()

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

    _B24_VALUES: typing.ClassVar[typing.Dict] = {
        True: TRUE,
        False: FALSE,
        None: DEFAULT,
    }

    __slots__ = ("_value",)

    def __init__(
            self,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, B24BoolStr, bool]],
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
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, B24BoolStr, bool]],
    ) -> typing.Optional[bool]:
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
    def value(self) -> typing.Optional[bool]:
        """"""
        return self._value

    @value.setter
    def value(
            self,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, B24BoolStr, bool]],
    ):
        """"""
        self._value = self._normalize(value)

    def to_b24(self) -> B24BoolLiteral:
        """"""
        return self._B24_VALUES[self._value]

    def to_str(self) -> typing.Text:
        """"""
        return str(self)

    @classmethod
    def from_b24(cls, value: B24BoolLiteral) -> "B24Bool":
        """"""
        return cls(value)
