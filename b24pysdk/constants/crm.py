from ..utils import enum as _enum


class EntityTypeAbbr(_enum.StrEnum):
    """Enumeration of CRM entity type abbreviations used in Bitrix24 CRM system."""
    LEAD = "L"
    DEAL = "D"
    CONTRACT = "C"
    COMPANY = "CO"
    INVOICE = "I"
    QUOTE = "Q"
    REQUISITE = "RQ"
    ORDER = "O"


class EntityTypeId(_enum.IntEnum):
    """Enumeration of CRM entity type IDs corresponding to Bitrix24 entities."""
    LEAD = 1
    DEAL = 2
    CONTRACT = 3
    COMPANY = 4
    INVOICE = 5
    QUOTE = 7
    REQUISITE = 8
    ORDER = 14


class EntityTypeName(_enum.StrEnum):
    """Enumeration of CRM entity type names corresponding to Bitrix24 entities."""
    LEAD = "LEAD"
    DEAL = "DEAL"
    CONTRACT = "CONTRACT"
    COMPANY = "COMPANY"
    INVOICE = "INVOICE"
    QUOTE = "QUOTE"
    REQUISITE = "REQUISITE"
    ORDER = "ORDER"


class UserFieldEntityId(_enum.StrEnum):
    """Enumeration of user field entity IDs for CRM entities in Bitrix24, used for custom fields identification."""
    LEAD = "CRM_LEAD"
    DEAL = "CRM_DEAL"
    CONTRACT = "CRM_CONTRACT"
    COMPANY = "CRM_COMPANY"
    INVOICE = "CRM_INVOICE"
    QUOTE = "CRM_QUOTE"
    REQUISITE = "CRM_REQUISITE"
    ORDER = "ORDER"
