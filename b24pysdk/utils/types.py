import typing

from .. import _constants

if _constants.PYTHON_VERSION >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self


__all__ = [
    "B24APIResult",
    "B24APIVersionLiteral",
    "B24AppStatusLiteral",
    "B24BoolLiteral",
    "B24BoolStrictLiteral",
    "B24File",
    "B24RequestTuple",
    "B24Requests",
    "DefaultTimeout",
    "DocumentType",
    "JSONDict",
    "JSONGenerator",
    "JSONList",
    "JSONValue",
    "Key",
    "Number",
    "ObjectDiscriminator",
    "Self",
    "Timeout",
    "cast",
]

_T = typing.TypeVar("_T")


def cast(_: typing.Type[_T], /, value: typing.Any) -> _T:
    """Cast value to the requested target type when it cannot be inferred statically."""
    return typing.cast("_T", value)


JSONDict = typing.Dict[typing.Text, typing.Any]
"""A JSON object represented as a dictionary with string keys."""

JSONGenerator = typing.Generator[JSONDict, None, None]
"""A generator yielding JSON dictionaries."""

JSONList = typing.List[JSONDict]
"""A JSON array represented as a list of JSON objects."""

JSONValue = typing.Union[bool, int, float, typing.Dict, typing.List, typing.Text]
"""
A non-null JSON-compatible value.

The alias is intentionally broad because Bitrix24 API methods may return
scalars, objects, or arrays depending on the REST method.
"""

Key = typing.Union[typing.Text, int]
"""A key that can be an integer or string used in dictionaries."""

Number = typing.Union[float, int]
"""A numeric type that can be either an integer or a float."""

ObjectDiscriminator = typing.Optional[
    typing.Union[
        typing.Hashable,
        typing.Tuple[typing.Hashable, ...],
    ]
]
"""A scalar or composite hashable discriminator used by the object registry."""

DefaultTimeout = typing.Union[Number, typing.Tuple[Number, Number]]
"""Timeout duration, represented as a single number or a tuple for connect and read timeouts."""

Timeout = typing.Optional[DefaultTimeout]
"""An optional timeout setting for API requests."""

B24APIResult = typing.Optional[JSONValue]
"""
Raw ``result`` payload returned by a Bitrix24 API call.

This is a broad fallback alias for untyped REST results. Concrete SDK methods
should prefer narrower generic annotations such as ``BitrixAPIRequest[List[Text]]``
or ``BitrixAPIRequest[JSONDict]`` when the exact result shape is known.
"""

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
"""Literal type for strict B24 boolean values: "Y" for Yes and "N" for No."""

B24RequestTuple = typing.Tuple[typing.Text, typing.Optional[JSONDict]]
"""Tuple containing a REST API method name and its optional parameters - (api_method, params)."""

B24Requests = typing.Union[typing.Mapping[Key, B24RequestTuple], typing.Sequence[B24RequestTuple]]
"""Batch request collection accepted by Bitrix24 batch calls."""


class DocumentType(tuple):
    """Represents a B24 document type which is always a list of 3 text elements."""

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
            raise TypeError(f"Invalid value for type {cls.__name__!r}: {value!r}")

        if not len(value) == cls.__AMOUNT_OF_VALUES:
            raise TypeError(f"{cls.__name__!r} must have exactly {cls.__AMOUNT_OF_VALUES} elements, got {len(value)}")

        return value

    def to_b24(self) -> typing.List[typing.Text]:
        """Return document type as list for Bitrix24 API."""
        return list(self)


class B24File(tuple):
    """Represents a B24 file which is always a list of 2 text elements (name, base64_content)"""

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
            raise TypeError(f"Invalid value for type {cls.__name__!r}: {value!r}")

        if not len(value) == cls.__AMOUNT_OF_VALUES:
            raise ValueError(f"{cls.__name__!r} must have exactly {cls.__AMOUNT_OF_VALUES} elements, got {len(value)}")

        return value

    def to_b24(self) -> typing.List[typing.Text]:
        """Return file as list for Bitrix24 API."""
        return list(self)
