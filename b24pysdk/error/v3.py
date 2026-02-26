import dataclasses as _dc
import functools as _ft
import typing

from .. import _constants
from . import BaseBitrixAPIError as _BaseBitrixAPIError
from ._http_response import HTTPResponseBadRequest, HTTPResponseUnauthorized

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
    """Bitrix v3 API error"""

    CODE: typing.ClassVar[typing.Text] = NotImplemented

    __slots__ = ()

    @_ft.cached_property
    def error(self) -> Error:
        """"""
        return Error.from_dict(self.json_response["error"])

    @_ft.cached_property
    def code(self) -> typing.Text:
        """"""
        return self.error.code

    @_ft.cached_property
    def validation(self) -> typing.Optional[typing.List[Validation]]:
        """"""
        return self.error.validation

    @property
    def has_validation(self) -> bool:
        """"""
        return bool(self.validation)


# Exceptions by status code

class BitrixAPIBadRequest(BitrixAPIError, HTTPResponseBadRequest):
    """Bad Request."""

    __slots__ = ()


class BitrixAPIUnauthorized(BitrixAPIError, HTTPResponseUnauthorized):
    """Unauthorized."""

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
