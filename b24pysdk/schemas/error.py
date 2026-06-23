from dataclasses import dataclass
from typing import List, Optional, Text, TypedDict, Union

from ..utils.dataclasses import frozen_dataclass_kwargs
from ._base_schema import BaseSchema

__all__ = [
    "ErrorData",
    "ErrorV1",
    "ErrorV1Data",
    "ErrorV3",
    "ErrorV3Data",
    "ErrorV3ErrorData",
    "ValidationItem",
    "ValidationItemData",
]


class _ErrorV1OptionalData(TypedDict, total=False):
    error_description: Text


class ErrorV1Data(_ErrorV1OptionalData):
    error: Text


@dataclass(**frozen_dataclass_kwargs())
class ErrorV1(BaseSchema[ErrorV1Data]):
    """
    Legacy Bitrix REST API error payload.

    API v1/v2 errors are returned as top-level ``error`` and optional
    ``error_description`` fields.
    """

    error: Text
    error_description: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: ErrorV1Data, /) -> "ErrorV1":
        """
        Create an ErrorV1 schema from legacy Bitrix24 error data.

        Args:
            bitrix_data: Raw legacy error payload.

        Returns:
            ErrorV1 schema with Python-friendly fields.
        """
        return cls(
            error=bitrix_data.get("error") or "",
            error_description=bitrix_data.get("error_description") or "",
        )

    def to_bitrix(self) -> ErrorV1Data:
        """
        Convert the schema back to a legacy Bitrix-compatible dictionary.

        Returns:
            Dictionary with legacy Bitrix24 error field names.
        """
        return {
            "error": self.error,
            "error_description": self.error_description,
        }


class ValidationItemData(TypedDict):
    field: Text
    message: Text


@dataclass(**frozen_dataclass_kwargs())
class ValidationItem(BaseSchema[ValidationItemData]):
    """
    Validation issue returned by Bitrix REST API v3.

    Represents a single field-level validation error with the field
    name and corresponding error message.
    """

    field: Text
    message: Text

    @classmethod
    def from_bitrix(cls, bitrix_data: ValidationItemData, /) -> "ValidationItem":
        """
        Create a Validation schema from Bitrix24 validation data.

        Args:
            bitrix_data: Raw v3 validation error item.

        Returns:
            Validation schema with field and message.
        """
        return cls(
            field=bitrix_data["field"],
            message=bitrix_data["message"],
        )

    def to_bitrix(self) -> ValidationItemData:
        """
        Convert the schema back to a Bitrix-compatible validation item.

        Returns:
            Dictionary with v3 validation field names.
        """
        return {
            "field": self.field,
            "message": self.message,
        }


class _ErrorV3ErrorOptionalData(TypedDict, total=False):
    validation: List[ValidationItemData]


class ErrorV3ErrorData(_ErrorV3ErrorOptionalData):
    code: Text
    message: Text


class ErrorV3Data(TypedDict):
    error: ErrorV3ErrorData


@dataclass(**frozen_dataclass_kwargs())
class ErrorV3(BaseSchema[ErrorV3Data]):
    """
    Structured Bitrix REST API v3 error payload.

    API v3 errors are returned as a top-level payload containing an ``error``
    object with code, message, and optional validation details.
    """

    code: Text
    message: Text
    validation: Optional[List[ValidationItem]]

    @classmethod
    def from_bitrix(cls, bitrix_data: ErrorV3Data, /) -> "ErrorV3":
        """
        Create an ErrorV3 schema from Bitrix24 v3 error data.

        Args:
            bitrix_data: Raw v3 error payload returned by REST API v3.

        Returns:
            ErrorV3 schema with optional validation details.
        """

        error_data = bitrix_data["error"]

        return cls(
            code=error_data["code"],
            message=error_data["message"],
            validation=[ValidationItem.from_bitrix(validation_item) for validation_item in error_data["validation"]] if "validation" in error_data else None,
        )

    def to_bitrix(self) -> ErrorV3Data:
        """
        Convert the schema back to a Bitrix-compatible v3 error object.

        Returns:
            Dictionary with v3 error field names.
        """

        error_data: ErrorV3ErrorData = {
            "code": self.code,
            "message": self.message,
        }

        if self.validation is not None:
            error_data["validation"] = [validation_item.to_bitrix() for validation_item in self.validation]

        return {
            "error": error_data,
        }


ErrorData = Union[ErrorV1Data, ErrorV3Data]
