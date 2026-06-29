from abc import ABC, abstractmethod
from typing import Any, Optional, Text, Union

from ..._config import Config
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...utils.types import B24APIVersionLiteral, JSONDict

__all__ = [
    "BaseCaller",
]


class BaseCaller(ABC):
    """
    Base class for low-level Bitrix API caller objects.

    A caller stores common request context: portal domain, authentication token,
    webhook/OAuth mode, target API method, request parameters, selected API
    version, and extra requester options. Subclasses implement ``call`` for a
    concrete transport pattern, for example a single method call, batch call, or
    paginated list call.
    """

    __slots__ = (
        "_api_method",
        "_api_version",
        "_auth_token",
        "_bitrix_token",
        "_config",
        "_domain",
        "_is_webhook",
        "_kwargs",
        "_params",
    )

    _config: Config
    _domain: Text
    _auth_token: Text
    _is_webhook: bool
    _api_method: Text
    _params: JSONDict
    _api_version: B24APIVersion
    _bitrix_token: Optional[BitrixTokenProtocol]
    _kwargs: JSONDict

    def __init__(
            self,
            *,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
            bitrix_token: Optional[BitrixTokenProtocol] = None,
            **kwargs,
    ):
        """
        Initialize shared caller state.

        Args:
            domain: Bitrix24 portal domain.
            auth_token: OAuth access token or webhook token.
            is_webhook: Whether ``auth_token`` is a webhook token.
            api_method: Bitrix REST method name.
            params: Method parameters passed to Bitrix.
            prefer_version: Preferred REST API version. V3 is used only when
                the method is registered as available in the SDK v3 method map.
            bitrix_token: Optional high-level token wrapper used to delegate
                nested calls through retry and token-refresh logic.
            **kwargs: Extra requester options, such as timeout and retry
                settings, forwarded to low-level requesters.
        """
        self._config = Config()
        self._domain = domain
        self._auth_token = auth_token
        self._is_webhook = is_webhook
        self._api_method = api_method
        self._params = params or {}
        self._api_version = self._resolve_api_version(api_method, prefer_version)
        self._bitrix_token = bitrix_token
        self._kwargs = kwargs

    def _resolve_api_version(
            self,
            api_method: Text,
            prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
    ) -> B24APIVersion:
        """
        Resolve the concrete API version used for this call.

        V3 is selected only when the caller explicitly prefers V3 and the method
        is present in the SDK configuration as a V3-capable method. All other
        calls fall back to V2 to preserve the existing REST behavior.
        """
        if prefer_version == B24APIVersion.V3 and self._config.is_api_v3_method(api_method):
            return B24APIVersion.V3
        else:
            return B24APIVersion.V2

    @abstractmethod
    def call(self) -> Any:
        """Execute the configured API operation and return the parsed response."""
        raise NotImplementedError
