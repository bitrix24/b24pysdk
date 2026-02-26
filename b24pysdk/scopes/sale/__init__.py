from functools import cached_property

from .._base_scope import BaseScope
from .basketitem import Basketitem
from .basketproperties import Basketproperties
from .businessvaluepersondomain import Businessvaluepersondomain
from .cashbox import Cashbox
from .delivery import Delivery
from .order import Order
from .payment import Payment
from .paymentitembasket import Paymentitembasket
from .paymentitemshipment import Paymentitemshipment
from .paysystem import Paysystem
from .persontype import Persontype
from .property import Property
from .propertygroup import Propertygroup
from .propertyrelation import Propertyrelation
from .propertyvalue import Propertyvalue
from .propertyvariant import Propertyvariant
from .shipment import Shipment
from .shipmentitem import Shipmentitem
from .shipmentproperty import Shipmentproperty
from .shipmentpropertyvalue import Shipmentpropertyvalue
from .status import Status
from .statuslang import Statuslang
from .tradebinding import Tradebinding
from .tradeplatform import Tradeplatform

__all__ = [
    "Sale",
]


class Sale(BaseScope):

    @cached_property
    def basketitem(self) -> Basketitem:
        """"""
        return Basketitem(self)

    @cached_property
    def basketproperties(self) -> Basketproperties:
        """"""
        return Basketproperties(self)

    @cached_property
    def businessvaluepersondomain(self) -> Businessvaluepersondomain:
        """"""
        return Businessvaluepersondomain(self)

    @cached_property
    def cashbox(self) -> Cashbox:
        """"""
        return Cashbox(self)

    @cached_property
    def delivery(self) -> Delivery:
        """"""
        return Delivery(self)

    @cached_property
    def order(self) -> Order:
        """"""
        return Order(self)

    @cached_property
    def payment(self) -> Payment:
        """"""
        return Payment(self)

    @cached_property
    def paymentitembasket(self) -> Paymentitembasket:
        """"""
        return Paymentitembasket(self)

    @cached_property
    def paymentitemshipment(self) -> Paymentitemshipment:
        """"""
        return Paymentitemshipment(self)

    @cached_property
    def paysystem(self) -> Paysystem:
        return Paysystem(self)

    @cached_property
    def persontype(self) -> Persontype:
        """"""
        return Persontype(self)

    @cached_property
    def property(self) -> Property:
        """"""
        return Property(self)

    @cached_property
    def propertygroup(self) -> Propertygroup:
        """"""
        return Propertygroup(self)

    @cached_property
    def propertyrelation(self) -> Propertyrelation:
        """"""
        return Propertyrelation(self)

    @cached_property
    def propertyvalue(self) -> Propertyvalue:
        """"""
        return Propertyvalue(self)

    @cached_property
    def propertyvariant(self) -> Propertyvariant:
        """"""
        return Propertyvariant(self)

    @cached_property
    def shipment(self) -> Shipment:
        """"""
        return Shipment(self)

    @cached_property
    def shipmentitem(self) -> Shipmentitem:
        """"""
        return Shipmentitem(self)

    @cached_property
    def shipmentproperty(self) -> Shipmentproperty:
        """"""
        return Shipmentproperty(self)

    @cached_property
    def shipmentpropertyvalue(self) -> Shipmentpropertyvalue:
        """"""
        return Shipmentpropertyvalue(self)

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @cached_property
    def statuslang(self) -> Statuslang:
        """"""
        return Statuslang(self)

    @cached_property
    def tradebinding(self) -> Tradebinding:
        """"""
        return Tradebinding(self)

    @cached_property
    def tradeplatform(self) -> Tradeplatform:
        """"""
        return Tradeplatform(self)
