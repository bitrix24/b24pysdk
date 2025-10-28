import typing

JSONDict = typing.Dict[typing.Text, typing.Any]
"""A dictionary with string keys and values of any type, typically used for JSON data structures."""

JSONList = typing.List[JSONDict]
"""A list containing dictionaries with string keys and values of any type, typically used for JSON data structures."""

Key = typing.Union[int, typing.Text]
"""A key that can be an integer or string used in dictionaries."""

Number = typing.Union[float, int]
"""A numeric type that can be either an integer or a float."""

DefaultTimeout = typing.Union[Number, typing.Tuple[Number, Number]]
"""Timeout duration, represented as a single number or a tuple for connect and read timeouts."""

Timeout = typing.Optional[DefaultTimeout]
"""An optional timeout setting for API requests."""

B24APIResult = typing.Optional[typing.Union[JSONDict, JSONList, bool]]
"""Represents the result of a Bitrix24 API call, which can be a dictionary, a list of dictionaries, or a boolean."""

B24AppStatusLiteral = typing.Literal["F", "D", "T", "P", "L", "S"]
"""Literal type for Bitrix24 application status codes:
'F' - Free
'D' - Demo
'T' - Trial
'P' - Paid
'L' - Local
'S' - Subscription
"""

B24BoolLiteral = typing.Literal["Y", "N", "D"]
"""Literal type for B24 boolean values: 'Y' for Yes, 'N' for No, and 'D' for Default."""

B24BatchMethodTuple = typing.Tuple[typing.Text, typing.Optional[JSONDict]]
"""Tuple containing a REST API method name and its optional parameters - (api_method, params)."""

B24BatchMethods = typing.Union[typing.Mapping[Key, B24BatchMethodTuple], typing.Sequence[B24BatchMethodTuple]]
""""""


class B24Bool:
    """Represents a B24 boolean value with a specific literal mapping."""

    _TRUE: B24BoolLiteral = "Y"
    _FALSE: B24BoolLiteral = "N"
    _DEFAULT: B24BoolLiteral = "D"

    _B24_BOOL_VALUES: typing.ClassVar[typing.Dict[typing.Optional[bool], B24BoolLiteral]] = {
        True: _TRUE,
        False: _FALSE,
        None: _DEFAULT,
    }

    __slots__ = ("_value",)

    def __init__(
            self,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, bool]],
    ):
        self._value = self._normalize(value)

    def __bool__(self):
        return bool(self._value)

    def __str__(self):
        return self.to_b24()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value})"

    def __eq__(
            self,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, bool]],
    ):
        return self._value == self._normalize(value)

    def __hash__(self):
        return hash(self._value)

    @classmethod
    def _normalize(
            cls,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, bool]],
    ) -> typing.Optional[bool]:
        """Normalize input value to a boolean for B24Bool."""

        if isinstance(value, cls):
            return value._value

        elif value is True or value == cls._TRUE:
            return True

        elif value is False or value == cls._FALSE:
            return False

        elif value is None or value == cls._DEFAULT:
            return None

        else:
            raise ValueError(f"Invalid value for type {cls.__name__!r}: {value!r}")

    @property
    def value(self) -> typing.Optional[bool]:
        """Return the internal boolean value."""
        return self._value

    @value.setter
    def value(
            self,
            value: typing.Optional[typing.Union["B24Bool", B24BoolLiteral, bool]],
    ):
        """Set the internal boolean value."""
        self._value = self._normalize(value)

    def to_b24(self) -> B24BoolLiteral:
        """Convert the internal boolean to a B24-compatible literal."""
        return self._B24_BOOL_VALUES[self._value]

    def to_str(self) -> B24BoolLiteral:
        """Return the B24 boolean as a string."""
        return typing.cast(B24BoolLiteral, str(self))

    @classmethod
    def from_b24(cls, value: B24BoolLiteral) -> "B24Bool":
        """Create a B24Bool instance from a B24 boolean literal."""
        return cls(value)
