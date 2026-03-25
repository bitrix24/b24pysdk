from ..utils import enum as _enum

__all__ = [
    "MessageDeliveryStatus",
]


class MessageDeliveryStatus(_enum.StrEnum):
    """Statuses for message delivery reports."""
    DELIVERED = "delivered"
    FAILED = "failed"
    UNDELIVERED = "undelivered"
