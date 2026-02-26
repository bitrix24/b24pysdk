from functools import cached_property

from .._base_scope import BaseScope
from .catalog import Catalog as CatalogEntity
from .document import Document
from .documentcontractor import Documentcontractor
from .enum import Enum
from .extra import Extra
from .measure import Measure
from .price import Price
from .price_type import PriceType
from .price_type_group import PriceTypeGroup
from .price_type_lang import PriceTypeLang
from .product import Product
from .product_image import ProductImage
from .product_property import ProductProperty
from .product_property_enum import ProductPropertyEnum
from .product_property_feature import ProductPropertyFeature
from .product_property_section import ProductPropertySection
from .ratio import Ratio
from .rounding_rule import RoundingRule
from .section import Section
from .store import Store
from .storeproduct import Storeproduct
from .userfield import Userfield
from .vat import Vat

__all__ = [
    "Catalog",
]


class Catalog(BaseScope):
    """"""

    @cached_property
    def catalog(self) -> CatalogEntity:
        """"""
        return CatalogEntity(self)

    @cached_property
    def document(self) -> Document:
        """"""
        return Document(self)

    @cached_property
    def documentcontractor(self) -> Documentcontractor:
        """"""
        return Documentcontractor(self)

    @cached_property
    def enum(self) -> Enum:
        """"""
        return Enum(self)

    @cached_property
    def extra(self) -> Extra:
        """"""
        return Extra(self)

    @cached_property
    def measure(self) -> Measure:
        """"""
        return Measure(self)

    @cached_property
    def price(self) -> Price:
        """"""
        return Price(self)

    @cached_property
    def price_type(self) -> PriceType:
        """"""
        return PriceType(self)

    @cached_property
    def price_type_group(self) -> PriceTypeGroup:
        """"""
        return PriceTypeGroup(self)

    @cached_property
    def price_type_lang(self) -> PriceTypeLang:
        """"""
        return PriceTypeLang(self)

    @cached_property
    def product(self) -> Product:
        """"""
        return Product(self)

    @cached_property
    def product_property(self) -> ProductProperty:
        """"""
        return ProductProperty(self)

    @cached_property
    def product_property_enum(self) -> ProductPropertyEnum:
        """"""
        return ProductPropertyEnum(self)

    @cached_property
    def product_property_feature(self) -> ProductPropertyFeature:
        """"""
        return ProductPropertyFeature(self)

    @cached_property
    def product_property_section(self) -> ProductPropertySection:
        """"""
        return ProductPropertySection(self)

    @cached_property
    def product_image(self) -> ProductImage:
        """"""
        return ProductImage(self)

    @cached_property
    def ratio(self) -> Ratio:
        """"""
        return Ratio(self)

    @cached_property
    def rounding_rule(self) -> RoundingRule:
        """"""
        return RoundingRule(self)

    @cached_property
    def section(self) -> Section:
        """"""
        return Section(self)

    @cached_property
    def store(self) -> Store:
        """"""
        return Store(self)

    @cached_property
    def storeproduct(self) -> Storeproduct:
        """"""
        return Storeproduct(self)

    @cached_property
    def userfield(self) -> Userfield:
        """"""
        return Userfield(self)

    @cached_property
    def vat(self) -> Vat:
        """"""
        return Vat(self)
