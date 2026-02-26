from functools import cached_property

from .._base_scope import BaseScope
from .agreement import Agreement
from .consent import Consent

__all__ = [
    "Userconsent",
]


class Userconsent(BaseScope):
    """"""

    @cached_property
    def agreement(self) -> Agreement:
        """"""
        return Agreement(self)

    @cached_property
    def consent(self) -> Consent:
        """"""
        return Consent(self)
