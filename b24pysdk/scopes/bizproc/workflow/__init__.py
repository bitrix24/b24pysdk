from functools import cached_property

from ..._base_entity import BaseEntity
from .template import Template

__all__ = [
    "Workflow",
]


class Workflow(BaseEntity):
    """"""

    @cached_property
    def template(self) -> Template:
        """"""
        return Template(self)
