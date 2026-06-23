from typing import Final, Optional, Text, Union

from ..._constants import MASKED_VALUE
from ...constants.version import B24APIVersion
from ...protocols import BitrixTokenProtocol
from ...utils.types import B24APIVersionLiteral, JSONDict, Timeout
from ._base_caller import BaseCaller
from .call import call

__all__ = [
    "call_method",
]


class _MethodCaller(BaseCaller):
    """Caller for one Bitrix REST method request."""

    _MASKED_AUTH: Final[Text] = MASKED_VALUE

    __slots__ = ()

    def __init__(
            self,
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
        Initialize a single-method caller.

        Args mirror ``call_method`` and are normalized by ``BaseCaller``. The
        caller later builds the correct REST URL for webhook/OAuth auth mode and
        for the selected API version.
        """
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=api_method,
            params=params,
            prefer_version=prefer_version,
            bitrix_token=bitrix_token,
            **kwargs,
        )

    @property
    def _dynamic_auth_token(self) -> Text:
        """
        Return the auth-token path fragment used by webhook URLs.

        Webhook calls include ``user_id/webhook_key`` in the URL path. OAuth
        calls pass the access token in request parameters, so this fragment is
        empty for OAuth mode.
        """
        return f"{self._auth_token}/" if self._is_webhook else ""

    @property
    def _base_url(self) -> Text:
        """Return the portal REST base URL, without method or auth suffix."""
        return f"https://{self._domain}/rest"

    @property
    def _url(self) -> Text:
        """
        Build the concrete method URL for the selected API version.

        V1/V2 calls use the classic ``/rest/{auth}/{method}.json`` format.
        V3 calls use ``/rest/api/{auth}/{method}`` and do not append ``.json``.
        """
        if self._api_version == B24APIVersion.V3:
            return f"{self._base_url}/api/{self._dynamic_auth_token}{self._api_method}"
        else:
            return f"{self._base_url}/{self._dynamic_auth_token}{self._api_method}.json"

    @property
    def _dynamic_params(self) -> JSONDict:
        """
        Return request parameters with OAuth auth injected when needed.

        Webhook authentication is already encoded in the URL, so webhook calls
        send only method parameters. OAuth calls add ``auth`` to the payload.
        """
        if self._is_webhook:
            return self._params
        else:
            return self._params | {"auth": self._auth_token}

    def _get_params_for_log(self) -> JSONDict:
        """Return method parameters prepared for logging."""

        if not self._config.secure_log or "auth" not in self._params:
            return self._params

        return self._params | {"auth": self._MASKED_AUTH}

    def call(self) -> JSONDict:
        """Execute the configured method request and log request/response context."""

        self._config.logger.debug(
            "start call_method",
            context={
                "domain": self._domain,
                "is_webhook": self._is_webhook,
                "method": self._api_method,
                "api_version": self._api_version,
                "params": self._get_params_for_log(),
            },
        )

        json_response = call(
            url=self._url,
            params=self._dynamic_params,
            **self._kwargs,
        )

        self._config.logger.debug(
            "finish call_method",
            context={
                "json_response": json_response,
            },
        )

        return json_response


def call_method(
        *,
        domain: Text,
        auth_token: Text,
        is_webhook: bool,
        api_method: Text,
        params: Optional[JSONDict] = None,
        timeout: Timeout = None,
        prefer_version: Union[B24APIVersion, B24APIVersionLiteral] = B24APIVersion.V2,
        bitrix_token: Optional[BitrixTokenProtocol] = None,
        **kwargs,
) -> JSONDict:
    """
    Call one Bitrix REST API method.

    The function builds a low-level method caller and returns the parsed JSON
    response from Bitrix. Webhook calls put the webhook token into the URL path;
    OAuth calls send the access token as the ``auth`` parameter. When
    ``prefer_version`` is V3 and the method is registered as V3-capable, the
    call uses the ``/rest/api/`` endpoint.

    Args:
        domain: Bitrix24 portal domain.
        auth_token: OAuth access token or webhook token.
        is_webhook: Whether ``auth_token`` is a webhook token.
        api_method: Bitrix REST method name, for example ``crm.deal.add``.
        params: Method parameters sent to Bitrix.
        timeout: Request timeout in seconds.
        prefer_version: Preferred API version to resolve the method against.
        bitrix_token: Optional high-level token wrapper used by nested calls.
        **kwargs: Extra requester options, such as retry configuration.

    Returns:
        Parsed Bitrix response containing method result and timing metadata.
    """
    return _MethodCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        api_method=api_method,
        params=params,
        timeout=timeout,
        prefer_version=prefer_version,
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
