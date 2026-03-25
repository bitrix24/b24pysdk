import dataclasses as _dc
import functools as _ft
import typing

from .. import _constants
from . import BaseBitrixAPIError as _BaseBitrixAPIError
from ._http_responses import HTTPResponseBadRequest, HTTPResponseUnauthorized

if typing.TYPE_CHECKING:
    from ..utils import types as _types

_DATACLASS_KWARGS = {"eq": False, "frozen": True}

if _constants.PYTHON_VERSION >= (3, 10):
    _DATACLASS_KWARGS["slots"] = True

__all__ = [
    "BitrixAPIAccessDeniedException",
    "BitrixAPIBadRequest",
    "BitrixAPIEntityNotFoundException",
    "BitrixAPIError",
    "BitrixAPIInvalidFilterException",
    "BitrixAPIInvalidPaginationException",
    "BitrixAPIUnauthorized",
    "BitrixAPIUnknownDTOPropertyException",
    "BitrixAPIValidationDTOValidationException",
    "BitrixAPIValidationRequestValidationException",
]


@_dc.dataclass(**_DATACLASS_KWARGS)
class Validation:
    """
    Validation issue returned by Bitrix REST API v3.

    Represents a single field-level validation error with the field
    name and corresponding error message.
    """

    field: typing.Text
    message: typing.Text

    @classmethod
    def from_dict(cls, json_response: "_types.JSONDict") -> "Validation":
        return cls(
            field=json_response["field"],
            message=json_response["message"],
        )

    def to_dict(self) -> "_types.JSONDict":
        return _dc.asdict(self)


@_dc.dataclass(**_DATACLASS_KWARGS)
class Error:
    """
    Structured API v3 error payload.

    Contains the machine-readable error code, a human-readable message,
    and optional validation details.
    """

    code: typing.Text
    message: typing.Text
    validation: typing.Optional[typing.List[Validation]]

    @classmethod
    def from_dict(cls, json_response: "_types.JSONDict") -> "Error":
        validation = json_response.get("validation")

        if isinstance(validation, list):
            validation = [Validation.from_dict(item) for item in validation]

        return cls(
            code=json_response["code"],
            message=json_response["message"],
            validation=validation,
        )

    def to_dict(self) -> "_types.JSONDict":
        return _dc.asdict(self)


# ------------------------ Exceptions for API v3 ------------------------


class BitrixAPIError(_BaseBitrixAPIError):
    """
    Bitrix REST API v3 error.

    Represents an API error returned by Bitrix REST API v3 where the error
    payload is structured as an `error` object rather than simple string
    fields used in earlier API versions.

    Typical response structure:

    {
        "error": {
            "code": "...",
            "message": "...",
            "validation": [...],
        },
    }

    The parsed error object is available via the `error` property.
    """

    CODE: typing.ClassVar[typing.Text] = NotImplemented

    __slots__ = ()

    @_ft.cached_property
    def error(self) -> Error:
        """
        Parsed error object returned by the API.

        Returns
        -------
        Error
            Structured representation of the API error parsed from the
            JSON response.
        """
        return Error.from_dict(self.json_response["error"])

    @property
    def code(self) -> typing.Text:
        """
        Error code returned by the API.

        Returns
        -------
        str
            Machine-readable error identifier provided by the API.
        """
        return self.error.code

    @property
    def validation(self) -> typing.Optional[typing.List[Validation]]:
        """
        Validation errors returned by the API.

        Returns
        -------
        Optional[List[Validation]]
            List of validation errors if the request failed validation,
            otherwise None.
        """
        return self.error.validation

    @property
    def has_validation(self) -> bool:
        """
        Check whether the error contains validation details.

        Returns
        -------
        bool
            True if validation errors are present in the response.
        """
        return bool(self.validation)


# Exceptions by status code

class BitrixAPIBadRequest(BitrixAPIError, HTTPResponseBadRequest):
    """Bad Request (400)."""

    __slots__ = ()


class BitrixAPIUnauthorized(BitrixAPIError, HTTPResponseUnauthorized):
    """Unauthorized (401)."""

    __slots__ = ()


# Exceptions by code

# 400

class BitrixAPIEntityNotFoundException(BitrixAPIBadRequest):
    """Entity not found."""

    CODE = "BITRIX_REST_V3_EXCEPTION_ENTITYNOTFOUNDEXCEPTION"

    __slots__ = ()


class BitrixAPIInvalidFilterException(BitrixAPIBadRequest):
    """Invalid filter."""

    CODE = "BITRIX_REST_V3_EXCEPTION_INVALIDFILTEREXCEPTION"

    __slots__ = ()


class BitrixAPIInvalidPaginationException(BitrixAPIBadRequest):
    """Invalid pagination."""

    CODE = "BITRIX_REST_V3_EXCEPTION_INVALIDPAGINATIONEXCEPTION"

    __slots__ = ()


class BitrixAPIUnknownDTOPropertyException(BitrixAPIBadRequest):
    """Unknown DTO property."""

    CODE = "BITRIX_REST_V3_EXCEPTION_UNKNOWNDTOPROPERTYEXCEPTION"

    __slots__ = ()


class BitrixAPIValidationDTOValidationException(BitrixAPIBadRequest):
    """DTO validation error."""

    CODE = "BITRIX_REST_V3_EXCEPTION_VALIDATION_DTOVALIDATIONEXCEPTION"

    __slots__ = ()


class BitrixAPIValidationRequestValidationException(BitrixAPIBadRequest):
    """Validation error."""

    CODE = "BITRIX_REST_V3_EXCEPTION_VALIDATION_REQUESTVALIDATIONEXCEPTION"

    __slots__ = ()


# 401

class BitrixAPIAccessDeniedException(BitrixAPIUnauthorized):
    """Access denied."""

    CODE = "BITRIX_REST_V3_EXCEPTION_ACCESSDENIEDEXCEPTION"

    __slots__ = ()
