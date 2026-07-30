from ..errors import BitrixSDKException


class BitrixObjectError(BitrixSDKException):
    """Base error for Bitrix object layer."""
    __slots__ = ()


class BitrixObjectDoesNotExist(BitrixObjectError):
    """Raised when a Bitrix object does not exist."""
    __slots__ = ()


class BitrixObjectMultipleObjectsReturned(BitrixObjectError):
    """Raised when a lookup returns more than one Bitrix object."""
    __slots__ = ()


class BitrixObjectClientError(BitrixObjectError):
    """Raised when a Bitrix client cannot be resolved."""
    __slots__ = ()


class BitrixObjectFieldError(BitrixObjectError):
    """Base error for Bitrix object field operations."""
    __slots__ = ()


class BitrixObjectFieldReadOnlyError(BitrixObjectFieldError):
    """Raised when a read-only object field is modified."""
    __slots__ = ()


class BitrixObjectFieldNotLoadedError(BitrixObjectFieldError):
    """Raised when an object field is not present in local Bitrix data."""
    __slots__ = ()
