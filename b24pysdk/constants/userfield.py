from ..utils import enum as _enum

__all__ = [
    "UserTypeID",
]


class UserTypeID(_enum.StrEnum):
    """Enum type ID for Bitrix24 user field types."""
    STRING = "string"
    INTEGER = "integer"
    DOUBLE = "double"
    DATE = "date"
    DATETIME = "datetime"
    BOOLEAN = "boolean"
    FILE = "file"
    ENUMERATION = "enumeration"
    URL = "url"
    ADDRESS = "address"
    MONEY = "money"
    IBLOCK_SECTION = "iblock_section"
    IBLOCK_ELEMENT = "iblock_element"
    EMPLOYEE = "employee"
    CRM = "crm"
    CRM_STATUS = "crm_status"
