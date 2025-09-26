import typing

JSONDict = typing.Dict[typing.Text, typing.Any]
"""A dictionary with string keys and values of any type, typically used for JSON data structures."""

JSONList = typing.List[JSONDict]
"""A list containing dictionaries with string keys and values of any type, typically used for JSON data structures."""

Key = typing.Union[int, typing.Text]
"""A key that can be an integer or string used in dictionaries."""

Number = typing.Union[int, float]
"""A numeric type that can be either an integer or a float."""

DefaultTimeout = typing.Union[Number, typing.Tuple[Number, Number]]
"""Timeout duration, represented as a single number or a tuple for connect and read timeouts."""

Timeout = typing.Optional[DefaultTimeout]
"""An optional timeout setting for API requests."""

B24APIResult = typing.Optional[typing.Union[JSONDict, JSONList, bool]]
"""Represents the result of a B24 API call, which can be a dictionary, a list of dictionaries, or a boolean."""

B24BatchRequestData = typing.Tuple[typing.Text, typing.Optional[JSONDict]]
"""Tuple containing a REST API method name and its optional parameters - (api_method, params)."""

B24BoolLiteral = typing.Literal["Y", "N", "D"]
"""Literal type for B24 boolean values: 'Y' for Yes, 'N' for No, and 'D' for Default."""


class B24BoolStr(str):
    """String subclass to represent B24 boolean values."""

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
    """Represents a B24 boolean value with a specific literal mapping."""
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
        """Normalize input value to a boolean for B24Bool."""
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
        """Return the internal boolean value."""
        return self._value

    @value.setter
    def value(
            self,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, B24BoolStr, bool]],
    ):
        """Set the internal boolean value."""
        self._value = self._normalize(value)

    def to_b24(self) -> B24BoolLiteral:
        """Convert the internal boolean to a B24-compatible literal."""
        return self._B24_VALUES[self._value]

    def to_str(self) -> typing.Text:
        """Return the B24 boolean as a string."""
        return str(self)

    @classmethod
    def from_b24(cls, value: B24BoolLiteral) -> "B24Bool":
        """Create a B24Bool instance from a B24 boolean literal."""
        return cls(value)
