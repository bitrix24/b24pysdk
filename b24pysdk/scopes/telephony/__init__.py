from functools import cached_property

from .._base_scope import BaseScope
from .call import Call
from .external_call import ExternalCall
from .external_line import ExternalLine
from .externalcall import Externalcall

__all__ = [
    "Telephony",
]


class Telephony(BaseScope):
    """"""

    @cached_property
    def call(self) -> Call:
        """"""
        return Call(self)

    @cached_property
    def external_call(self) -> ExternalCall:
        """"""
        return ExternalCall(self)

    @cached_property
    def external_line(self) -> ExternalLine:
        """"""
        return ExternalLine(self)

    @cached_property
    def externalcall(self) -> Externalcall:
        """"""
        return Externalcall(self)
