from typing import TYPE_CHECKING

from ..scope import Scope
from .activity import Activity
from .address import Address
from .automatedsolution import Automatedsolution
from .automation import Automation
from .calllist import Calllist
from .category import Category
from .company import Company
from .contact import Contact
from .currency import Currency
from .deal import Deal
from .documentgenerator import Documentgenerator
from .duplicate import Duplicate, Entity
from .enum import Enum
from .item import Item
from .lead import Lead
from .multifield import Multifield
from .orderentity import Orderentity
from .quote import Quote
from .requisite import Requisite
from .stagehistory import Stagehistory
from .status import Status
from .timeline import Timeline
from .type import Type
from .userfield import Userfield
from .vat import Vat

if TYPE_CHECKING:
    from ... import Client

__all__ = [
    "CRM",
]


class CRM(Scope):
    """"""

    __slots__ = (
        "activity",
        "address",
        "automatedsolution",
        "automation",
        "calllist",
        "category",
        "company",
        "contact",
        "currency",
        "deal",
        "documentgenerator",
        "duplicate",
        "entity",
        "enum",
        "item",
        "lead",
        "multifield",
        "orderentity",
        "quote",
        "requisite",
        "stagehistory",
        "status",
        "timeline",
        "type",
        "userfield",
        "vat",
    )

    activity: Activity
    address: Address
    automatedsolution: Automatedsolution
    automation: Automation
    calllist: Calllist
    category: Category
    company: Company
    contact: Contact
    currency: Currency
    deal: Deal
    documentgenerator: Documentgenerator
    duplicate: Duplicate
    entity: Entity
    enum: Enum
    item: Item
    lead: Lead
    multifield: Multifield
    orderentity: Orderentity
    quote: Quote
    requisite: Requisite
    stagehistory: Stagehistory
    status: Status
    timeline: Timeline
    type: Type
    userfield: Userfield
    vat: Vat

    def __init__(self, client: "Client"):
        super().__init__(client)
        self.activity = Activity(self)
        self.address = Address(self)
        self.automatedsolution = Automatedsolution(self)
        self.automation = Automation(self)
        self.calllist = Calllist(self)
        self.category = Category(self)
        self.company = Company(self)
        self.contact = Contact(self)
        self.currency = Currency(self)
        self.deal = Deal(self)
        self.documentgenerator = Documentgenerator(self)
        self.duplicate = Duplicate(self)
        self.entity = Entity(self)
        self.enum = Enum(self)
        self.item = Item(self)
        self.lead = Lead(self)
        self.multifield = Multifield(self)
        self.orderentity = Orderentity(self)
        self.quote = Quote(self)
        self.requisite = Requisite(self)
        self.stagehistory = Stagehistory(self)
        self.status = Status(self)
        self.timeline = Timeline(self)
        self.type = Type(self)
        self.userfield = Userfield(self)
        self.vat = Vat(self)
