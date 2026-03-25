from ..utils import enum as _enum

__all__ = [
    "TelephonyAddToChat",
    "TelephonyCallType",
    "TelephonyCrmAutoCreate",
    "TelephonyCrmEntityType",
    "TelephonyExternalCallStatusCode",
    "TelephonyVote",
]


class TelephonyCrmAutoCreate(_enum.StrEnum):
    """CRM auto-create mode for telephony.externalLine.*."""
    ENABLED = "Y"
    DISABLED = "N"


class TelephonyCallType(_enum.IntEnum):
    """Call type values for telephony.externalCall.register."""
    OUTGOING = 1
    INCOMING = 2
    INCOMING_REDIRECTED = 3
    CALLBACK = 4
    INFOCALL = 5


class TelephonyCrmEntityType(_enum.StrEnum):
    """CRM entity types for telephony.externalCall.register."""
    CONTACT = "CONTACT"
    COMPANY = "COMPANY"
    LEAD = "LEAD"


class TelephonyExternalCallStatusCode(_enum.StrEnum):
    """Status codes for telephony.externalCall.finish."""
    SUCCESS = "200"
    MISSED = "304"
    DECLINED = "603"
    CANCELED = "603-S"
    FORBIDDEN = "403"
    WRONG_NUMBER = "404"
    BUSY = "486"
    ROUTE_UNAVAILABLE = "484"
    ROUTE_UNAVAILABLE_ALT = "503"
    TEMP_UNAVAILABLE = "480"
    INSUFFICIENT_FUNDS = "402"
    BLOCKED = "423"
    OTHER = "OTHER"


class TelephonyVote(_enum.IntEnum):
    """Call rating values for telephony.externalCall.finish."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5


class TelephonyAddToChat(_enum.IntEnum):
    """Chat message behavior for telephony.externalCall.finish."""
    NO = 0
    YES = 1
