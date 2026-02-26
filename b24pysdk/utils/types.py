import typing

from ..error import BitrixValidationError

__all__ = [
    "B24APIResult",
    "B24APIVersionLiteral",
    "B24AppStatusLiteral",
    "B24Bool",
    "B24BoolLiteral",
    "B24BoolStrict",
    "B24BoolStrictLiteral",
    "B24File",
    "B24RequestTuple",
    "B24Requests",
    "DefaultTimeout",
    "DocumentType",
    "JSONDict",
    "JSONDictGenerator",
    "JSONList",
    "Key",
    "Number",
    "Timeout",
    "UserTypeIDLiteral",
]

JSONDict = typing.Dict[typing.Text, typing.Any]
"""A dictionary with string keys and values of any type, typically used for JSON data structures."""

JSONDictGenerator = typing.Generator[JSONDict, None, None]
""""""

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

B24APIVersionLiteral = typing.Literal[1, 2, 3]
"""Supported Bitrix API versions."""

B24AppStatusLiteral = typing.Literal["F", "D", "T", "P", "L", "S"]
"""Literal type for Bitrix24 application status codes:\n
"F" - Free\n
"D" - Demo\n
"T" - Trial\n
"P" - Paid\n
"L" - Local\n
"S" - Subscription
"""

B24BoolLiteral = typing.Literal["D", "N", "Y"]
"""Literal type for B24 boolean values: "Y" for Yes, "N" for No, and "D" for Default."""

B24BoolStrictLiteral = typing.Literal["N", "Y"]
""""""

B24RequestTuple = typing.Tuple[typing.Text, typing.Optional[JSONDict]]
"""Tuple containing a REST API method name and its optional parameters - (api_method, params)."""

B24Requests = typing.Union[typing.Mapping[Key, B24RequestTuple], typing.Sequence[B24RequestTuple]]
""""""

UserTypeIDLiteral = typing.Literal[
    "string",
    "integer",
    "double",
    "date",
    "datetime",
    "boolean",
    "file",
    "enumeration",
    "url",
    "address",
    "money",
    "iblock_section",
    "iblock_element",
    "employee",
    "crm",
    "crm_status",
]
"""Literal type ID for Bitrix24 user field types:\n
"string"          — string\n
"integer"         — integer\n
"double"          — double/float\n
"date"            — date\n
"datetime"        — date with time\n
"boolean"         — yes/no\n
"file"            — file\n
"enumeration"     — list/enumeration\n
"url"             — URL/link\n
"address"         — Google Maps address\n
"money"           — money/currency\n
"iblock_section"  — iblock section reference\n
"iblock_element"  — iblock element reference\n
"employee"        — employee/user reference\n
"crm"             — CRM entity reference\n
"crm_status"      — CRM status reference
"""


class B24Bool:
    """Represents a B24 boolean value with a specific literal mapping."""

    class ValidationError(BitrixValidationError):
        """"""

    __B24_DEFAULT: B24BoolLiteral = "D"
    __B24_FALSE: B24BoolLiteral = "N"
    __B24_TRUE: B24BoolLiteral = "Y"

    _B24_BOOL_VALUES: typing.ClassVar[typing.Dict[typing.Optional[bool], typing.Text]] = {
        None: __B24_DEFAULT,
        False: __B24_FALSE,
        True: __B24_TRUE,
    }

    __slots__ = ("_value",)

    _value: typing.Optional[bool]

    def __init__(
            self,
            value: typing.Optional[typing.Union["B24Bool", typing.Annotated[typing.Text, B24BoolLiteral], bool]],
    ):
        self._value = self._validate(value)

    def __bool__(self):
        return bool(self._value)

    def __str__(self):
        return self.to_b24()

    def __repr__(self):
        return f"{self.__class__.__name__}({self._value})"

    def __hash__(self):
        return hash(self._value)

    def __eq__(
            self,
            other: typing.Optional[typing.Union["B24Bool", typing.Annotated[typing.Text, B24BoolLiteral], bool]],
    ):
        return self._value == self._validate(other)

    def __and__(
            self,
            other: typing.Optional[typing.Union["B24Bool", typing.Annotated[typing.Text, B24BoolLiteral], bool]],
    ):
        return self._value and self._validate(other)

    def __or__(
            self,
            other: typing.Optional[typing.Union["B24Bool", typing.Annotated[typing.Text, B24BoolLiteral], bool]],
    ):
        return self._value or self._validate(other)

    @classmethod
    def _validate(
            cls,
            value: typing.Optional[typing.Union["B24Bool", typing.Annotated[typing.Text, B24BoolLiteral], bool]],
    ) -> typing.Optional[bool]:
        """Normalize input value to a boolean for B24Bool."""

        if isinstance(value, cls):
            return value._value

        elif value is None or value == cls.__B24_DEFAULT:
            return None

        elif value is False or value == cls.__B24_FALSE:
            return False

        elif value is True or value == cls.__B24_TRUE:
            return True

        else:
            raise cls.ValidationError(f"Invalid value for type {cls.__name__!r}: {value!r}")

    @classmethod
    def from_b24(cls, value: typing.Annotated[typing.Text, B24BoolLiteral]) -> "B24Bool":
        """Create a B24Bool instance from a B24 boolean literal."""
        return cls(value)

    def to_b24(self) -> B24BoolLiteral:
        """Convert the internal boolean to a B24-compatible literal."""
        return typing.cast("B24BoolLiteral", self._B24_BOOL_VALUES[self._value])


class B24BoolStrict(B24Bool):
    """"""

    __B24_FALSE: B24BoolStrictLiteral = "N"
    __B24_TRUE: B24BoolStrictLiteral = "Y"

    _B24_BOOL_VALUES: typing.ClassVar[typing.Dict[bool, typing.Text]] = {
        False: __B24_FALSE,
        True: __B24_TRUE,
    }

    __slots__ = ()

    _value: bool

    def __init__(
            self,
            value: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], bool],
    ):
        super().__init__(value)

    def __int__(self):
        return int(self._value)

    def __index__(self):
        return int(self)

    def __float__(self):
        return float(self._value)

    def __lt__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value < self._validate_as_number(other)

    def __le__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value <= self._validate_as_number(other)

    def __gt__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__class__(other) < self

    def __ge__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__class__(other) <= self

    def __pos__(self):
        return +self._value

    def __neg__(self):
        return -self._value

    def __add__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value + self._validate_as_number(other)

    def __radd__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__add__(other)

    def __sub__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value - self._validate_as_number(other)

    def __rsub__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__class__(other) - self

    def __mul__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value * self._validate_as_number(other)

    def __rmul__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__mul__(other)

    def __truediv__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value / self._validate_as_number(other)

    def __rtruediv__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__class__(other) / self

    def __floordiv__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value // self._validate_as_number(other)

    def __rfloordiv__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__class__(other) // self

    def __mod__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self._value % self._validate_as_number(other)

    def __rmod__(
            self,
            other: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ):
        return self.__class__(other) % self

    @classmethod
    def _validate(
            cls,
            value: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ) -> bool:
        """"""

        if isinstance(value, cls):
            return value._value

        elif value is False or value == cls.__B24_FALSE:
            return False

        elif value is True or value == cls.__B24_TRUE:
            return True

        else:
            raise cls.ValidationError(f"Invalid value for type {cls.__name__!r}: {value!r}")

    @classmethod
    def _validate_as_number(
            cls,
            value: typing.Union["B24BoolStrict", typing.Annotated[typing.Text, B24BoolStrictLiteral], Number],
    ) -> Number:
        """"""
        if isinstance(value, (float, int)):
            return value
        else:
            return cls._validate(value)

    @property
    def value(self) -> bool:
        """"""
        return self._value

    @classmethod
    def from_b24(cls, value: typing.Annotated[typing.Text, B24BoolStrictLiteral]) -> "B24BoolStrict":
        """"""
        return cls(value)

    def to_b24(self) -> B24BoolStrictLiteral:
        """"""
        return typing.cast("B24BoolStrictLiteral", super().to_b24())


class DocumentType(tuple):
    """Represents a B24 document type which is always a list of 3 text elements."""

    class ValidationError(BitrixValidationError):
        """"""

    __AMOUNT_OF_VALUES: int = 3

    __slots__ = ()

    def __new__(cls, value: typing.Sequence[typing.Text]):
        return super().__new__(cls, cls._validate(value))

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    @property
    def module(self) -> typing.Text:
        return self[0]

    @property
    def document(self) -> typing.Text:
        return self[1]

    @property
    def entity(self) -> typing.Text:
        return self[2]

    @classmethod
    def _validate(cls, value: typing.Sequence[typing.Text]) -> typing.Sequence[typing.Text]:
        """Validate document type value."""

        if not isinstance(value, typing.Sequence):
            raise cls.ValidationError(f"Invalid value for type {cls.__name__!r}: {value!r}")

        if not len(value) == cls.__AMOUNT_OF_VALUES:
            raise cls.ValidationError(f"{cls.__name__!r} must have exactly {cls.__AMOUNT_OF_VALUES} elements, got {len(value)}")

        return value

    def to_b24(self) -> typing.List[typing.Text]:
        """Return document type as list for Bitrix24 API."""
        return list(self)


class B24File(tuple):
    """Represents a B24 file which is always a list of 2 text elements (name, base64_content)"""

    class ValidationError(BitrixValidationError):
        """"""

    __AMOUNT_OF_VALUES: int = 2

    __slots__ = ()

    def __new__(cls, value: typing.Sequence[typing.Text]):
        return super().__new__(cls, cls._validate(value))

    def __repr__(self):
        return f"{self.__class__.__name__}({super().__repr__()})"

    @property
    def filename(self) -> typing.Text:
        return self[0]

    @property
    def content(self) -> typing.Text:
        return self[1]

    @classmethod
    def _validate(cls, value: typing.Sequence[typing.Text]) -> typing.Sequence[typing.Text]:

        if not isinstance(value, typing.Sequence):
            raise cls.ValidationError(f"Invalid value for type {cls.__name__!r}: {value!r}")

        if not len(value) == cls.__AMOUNT_OF_VALUES:
            raise cls.ValidationError(f"{cls.__name__!r} must have exactly {cls.__AMOUNT_OF_VALUES} elements, got {len(value)}")

        return value

    def to_b24(self) -> typing.List[typing.Text]:
        """Return file as list for Bitrix24 API."""
        return list(self)
