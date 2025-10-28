from typing import Optional, Protocol, Text

from ...utils.types import JSONDict, Timeout


class BitrixTokenProtocol(Protocol):
    """"""

    domain: Text
    is_webhook: bool
    auth_token: Text
    refresh_token: Optional[Text]

    def call_method(
            self,
            api_method: Text,
            params: Optional[JSONDict] = None,
            *,
            timeout: Timeout = None,
            **kwargs,
    ) -> JSONDict: ...
