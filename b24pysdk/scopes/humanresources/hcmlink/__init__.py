from functools import cached_property

from ..._base_entity import BaseEntity
from .company import Company
from .employee import Employee
from .field import Field
from .job import Job

__all__ = [
    "Hcmlink",
]


class Hcmlink(BaseEntity):
    """"""

    @cached_property
    def company(self) -> Company:
        """"""
        return Company(self)

    @cached_property
    def employee(self) -> Employee:
        """"""
        return Employee(self)

    @cached_property
    def field(self) -> Field:
        """"""
        return Field(self)

    @cached_property
    def job(self) -> Job:
        """"""
        return Job(self)
