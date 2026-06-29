import typing as _tp

from .._constants import MISSING
from ..schemas import error as _error_schemas
from . import BitrixBaseAPIBadRequest as _BitrixBaseAPIBadRequest
from . import BitrixBaseAPIError as _BaseBitrixAPIError
from . import BitrixBaseAPIUnauthorized as _BitrixBaseAPIUnauthorized

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

    CODE: _tp.ClassVar[_tp.Text] = MISSING

    __slots__ = ()

    json_response: _error_schemas.ErrorV3Data

    @property
    def error(self) -> "_error_schemas.ErrorV3":
        """
        Parsed error object returned by the API.

        Returns
        -------
        ErrorV3
            Structured representation of the API error parsed from the
            JSON response.
        """
        return _error_schemas.ErrorV3.from_bitrix(self.json_response)

    @property
    def code(self) -> _tp.Text:
        """
        Error code returned by the API.

        Returns
        -------
        str
            Machine-readable error identifier provided by the API.
        """
        return self.error.code

    @property
    def validation(self) -> _tp.Optional[_tp.List["_error_schemas.ValidationItem"]]:
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

class BitrixAPIBadRequest(_BitrixBaseAPIBadRequest, BitrixAPIError):
    """Bad Request (400)."""

    __slots__ = ()


class BitrixAPIUnauthorized(_BitrixBaseAPIUnauthorized, BitrixAPIError):
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
