from ..utils import enum as _enum

__all__ = [
    "DeliveryExtraServiceType",
    "OrderPropertyType",
    "PaysystemEntityRegistryType",
    "SaleStatusType",
]


class PaysystemEntityRegistryType(_enum.StrEnum):
    """Entity registry bindings for sale.paysystem.add."""
    ORDER = "ORDER"
    CRM_INVOICE = "CRM_INVOICE"
    CRM_QUOTE = "CRM_QUOTE"


class SaleStatusType(_enum.StrEnum):
    """Status type for sale.status.add fields.sale_status.type."""
    ORDER = "O"
    DELIVERY = "D"


class OrderPropertyType(_enum.StrEnum):
    """Property types for sale.property.add fields.sale_order_property.type."""
    STRING = "STRING"
    YES_NO = "Y/N"
    NUMBER = "NUMBER"
    ENUM = "ENUM"
    FILE = "FILE"
    DATE = "DATE"
    LOCATION = "LOCATION"
    ADDRESS = "ADDRESS"


class DeliveryExtraServiceType(_enum.StrEnum):
    """Service types for sale.delivery.extra.service.add TYPE."""
    ENUM = "enum"
    CHECKBOX = "checkbox"
    QUANTITY = "quantity"
