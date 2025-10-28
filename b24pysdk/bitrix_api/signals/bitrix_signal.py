from typing import TYPE_CHECKING, Type

from psygnal import Signal, SignalInstance

if TYPE_CHECKING:
    from ..events import BaseBitrixEvent


class BitrixSignalInstance(SignalInstance):
    """"""

    @classmethod
    def create_signal(cls, event_class: Type["BaseBitrixEvent"]) -> Signal:
        return Signal(event_class, signal_instance_class=cls)
