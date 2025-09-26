from typing import TYPE_CHECKING, Type

from psygnal import Signal, SignalInstance

if TYPE_CHECKING:
    from ..events import BaseBitrixEvent


class BitrixSignalInstance(SignalInstance):
    """"""


def create_bitrix_signal(event_class: Type["BaseBitrixEvent"]) -> Signal:
    return Signal(event_class, signal_instance_class=BitrixSignalInstance)
