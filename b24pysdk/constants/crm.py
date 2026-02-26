from ..utils import enum as _enum

__all__ = [
    "ActivityDirection",
    "ActivityNotifyType",
    "ActivityPriority",
    "ActivityStatus",
    "ActivityType",
    "AddressType",
    "CRMSettingsMode",
    "ContentType",
    "EntityTypeAbbr",
    "EntityTypeID",
    "EntityTypeName",
    "SemanticID",
    "UserFieldEntityID",
]


class ActivityDirection(_enum.IntEnum):
    """CRM activity direction used in Bitrix24."""
    INCOMING = 1
    OUTGOING = 2


class ActivityNotifyType(_enum.IntEnum):
    """CRM activity notify time units used in Bitrix24."""
    MINUTES = 1
    HOURS = 2
    DAYS = 3


class ActivityPriority(_enum.IntEnum):
    """CRM activity priority used in Bitrix24."""
    LOW = 1
    NORMAL = 2
    HIGH = 3


class ActivityStatus(_enum.IntEnum):
    """CRM activity status used in Bitrix24."""
    PENDING = 1
    COMPLETED = 2
    AUTO_COMPLETED = 3


class ActivityType(_enum.IntEnum):
    """CRM activity type used in Bitrix24."""
    MEETING = 1
    CALL = 2
    TASK = 3
    EMAIL = 4
    ACTION = 5
    CUSTOM_ACTION = 6


class AddressType(_enum.IntEnum):
    """"""
    ACTUAL = 1
    REGISTRATION = 4
    LEGAL = 6
    MAILING = 8
    BENEFICIARY = 9
    DELIVERY = 11


class CRMSettingsMode(_enum.IntEnum):
    """"""
    CLASSIC = 1
    SIMPLE = 2


class ContentType(_enum.IntEnum):
    """Content type for CRM activities/messages in Bitrix24."""
    PLAIN_TEXT = 1
    BBCODE = 2
    HTML = 3


class EntityTypeAbbr(_enum.StrEnum):
    """Enumeration of CRM entity type abbreviations used in Bitrix24 CRM system."""
    LEAD = "L"
    DEAL = "D"
    CONTACT = "C"
    COMPANY = "CO"
    INVOICE = "I"
    QUOTE = "Q"
    REQUISITE = "RQ"
    ORDER = "O"
    SMART_INVOICE = "SI"
    SMART_DOCUMENT = "DO"
    SMART_B2E_DOC = "SBD"


class EntityTypeID(_enum.IntEnum):
    """Enumeration of CRM entity type IDs corresponding to Bitrix24 entities."""
    LEAD = 1
    DEAL = 2
    CONTACT = 3
    COMPANY = 4
    INVOICE = 5
    QUOTE = 7
    REQUISITE = 8
    ORDER = 14
    SMART_INVOICE = 31
    SMART_DOCUMENT = 36
    SMART_B2E_DOC = 39


class EntityTypeName(_enum.StrEnum):
    """Enumeration of CRM entity type names corresponding to Bitrix24 entities."""
    LEAD = "LEAD"
    DEAL = "DEAL"
    CONTACT = "CONTACT"
    COMPANY = "COMPANY"
    INVOICE = "INVOICE"
    QUOTE = "QUOTE"
    REQUISITE = "REQUISITE"
    ORDER = "ORDER"
    SMART_INVOICE = "SMART_INVOICE"
    SMART_DOCUMENT = "SMART_DOCUMENT"
    SMART_B2E_DOC = "SMART_B2E_DOC"


class SemanticID(_enum.StrEnum):
    """CRM semantic IDs used in Bitrix24 (stage semantics)."""
    PROCESS = "P"
    SUCCESS = "S"
    FAILURE = "F"


class UserFieldEntityID(_enum.StrEnum):
    """Enumeration of user field entity IDs for CRM entities in Bitrix24, used for custom fields identification."""
    LEAD = "CRM_LEAD"
    DEAL = "CRM_DEAL"
    CONTACT = "CRM_CONTRACT"
    COMPANY = "CRM_COMPANY"
    INVOICE = "CRM_INVOICE"
    QUOTE = "CRM_QUOTE"
    REQUISITE = "CRM_REQUISITE"
    ORDER = "ORDER"
