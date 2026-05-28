from typing import Protocol, Text


class BitrixOAuthProtocol(Protocol):
    """
    Protocol for objects that provide Bitrix24 OAuth application credentials.

    Used to type objects that expose OAuth client ID and client secret.
    """

    client_id: Text
    """OAuth client ID issued by Bitrix24."""

    client_secret: Text
    """OAuth client secret issued by Bitrix24."""
