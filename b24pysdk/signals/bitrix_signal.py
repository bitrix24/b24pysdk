from typing import TYPE_CHECKING, Type

from psygnal import Signal, SignalInstance

if TYPE_CHECKING:
    from ..events import BaseBitrixEvent


class BitrixSignalInstance(SignalInstance):
    """
    Custom signal instance for Bitrix24 event dispatching.

    Extends psygnal's SignalInstance and provides a helper for creating
    strongly typed signals bound to Bitrix event classes.
    """

    @classmethod
    def create_signal(cls, event_class: Type["BaseBitrixEvent"]) -> Signal:
        """
        Create a signal for the given Bitrix event class.

        Args:
            event_class: Bitrix event class used as the signal argument type.

        Returns:
            Signal configured to use BitrixSignalInstance.
        """
        return Signal(event_class, signal_instance_class=cls)
