import typing

from ..utils import enum as _enum

__all__ = [
    "UserTypeID",
    "UserTypeIDLiteral",
]


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
