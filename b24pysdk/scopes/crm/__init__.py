from ..scope import Scope

from .activity import Activity
from .address import Address
from .category import Category
from .company import Company
from .contact import Contact
from .deal import Deal
from .item import Item
from .lead import Lead
from .orderentity import Orderentity
from .quote import Quote
from .requisite import Requisite
from .timeline import Timeline
from .type import Type
from .userfield import Userfield


class CRM(Scope):
    """"""

    __slots__ = (
        "activity",
        "address",
        "category",
        "company",
        "contact",
        "deal",
        "item",
        "lead",
        "orderentity",
        "quote",
        "requisite",
        "timeline",
        "type",
        "userfield",
    )

    activity: Activity
    address: Address
    category: Category
    company: Company
    contact: Contact
    deal: Deal
    item: Item
    lead: Lead
    orderentity: Orderentity
    quote: Quote
    requisite: Requisite
    timeline: Timeline
    type: Type
    userfield: Userfield

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activity = Activity(self)
        self.address = Address(self)
        self.category = Category(self)
        self.company = Company(self)
        self.contact = Contact(self)
        self.deal = Deal(self)
        self.item = Item(self)
        self.lead = Lead(self)
        self.orderentity = Orderentity(self)
        self.quote = Quote(self)
        self.requisite = Requisite(self)
        self.timeline = Timeline(self)
        self.type = Type(self)
        self.userfield = Userfield(self)


__all__ = [
    "CRM",
]
