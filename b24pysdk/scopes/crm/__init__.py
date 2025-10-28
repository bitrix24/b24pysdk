from functools import cached_property

from .._base_scope import BaseScope
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
from .duplicate import Duplicate
from .entity import Entity
from .enum import Enum
from .item import Item
from .lead import Lead
from .multifield import Multifield
from .orderentity import Orderentity
from .quote import Quote
from .requisite import Requisite
from .settings import Settings
from .stagehistory import Stagehistory
from .status import Status
from .timeline import Timeline
from .type import Type
from .userfield import Userfield
from .vat import Vat

__all__ = [
    "CRM",
]


class CRM(BaseScope):
    """"""

    @cached_property
    def activity(self) -> Activity:
        """"""
        return Activity(self)

    @cached_property
    def address(self) -> Address:
        """"""
        return Address(self)

    @cached_property
    def automatedsolution(self) -> Automatedsolution:
        """"""
        return Automatedsolution(self)

    @cached_property
    def automation(self) -> Automation:
        """"""
        return Automation(self)

    @cached_property
    def calllist(self) -> Calllist:
        """"""
        return Calllist(self)

    @cached_property
    def category(self) -> Category:
        """"""
        return Category(self)

    @cached_property
    def company(self) -> Company:
        """"""
        return Company(self)

    @cached_property
    def contact(self) -> Contact:
        """"""
        return Contact(self)

    @cached_property
    def currency(self) -> Currency:
        """"""
        return Currency(self)

    @cached_property
    def deal(self) -> Deal:
        """"""
        return Deal(self)

    @cached_property
    def documentgenerator(self) -> Documentgenerator:
        """"""
        return Documentgenerator(self)

    @cached_property
    def duplicate(self) -> Duplicate:
        """"""
        return Duplicate(self)

    @cached_property
    def entity(self) -> Entity:
        """"""
        return Entity(self)

    @cached_property
    def enum(self) -> Enum:
        """"""
        return Enum(self)

    @cached_property
    def item(self) -> Item:
        """"""
        return Item(self)

    @cached_property
    def lead(self) -> Lead:
        """"""
        return Lead(self)

    @cached_property
    def multifield(self) -> Multifield:
        """"""
        return Multifield(self)

    @cached_property
    def orderentity(self) -> Orderentity:
        """"""
        return Orderentity(self)

    @cached_property
    def quote(self) -> Quote:
        """"""
        return Quote(self)

    @cached_property
    def requisite(self) -> Requisite:
        """"""
        return Requisite(self)

    @cached_property
    def settings(self) -> Settings:
        """"""
        return Settings(self)

    @cached_property
    def stagehistory(self) -> Stagehistory:
        """"""
        return Stagehistory(self)

    @cached_property
    def status(self) -> Status:
        """"""
        return Status(self)

    @cached_property
    def timeline(self) -> Timeline:
        """"""
        return Timeline(self)

    @cached_property
    def type(self) -> Type:
        """"""
        return Type(self)

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @cached_property
    def vat(self) -> Vat:
        """"""
        return Vat(self)
