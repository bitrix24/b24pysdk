from typing import Optional, Text

from ...utils.types import JSONDict, Timeout
from ..protocols import BitrixTokenProtocol
from ._base_caller import BaseCaller
from .call import call


class _MethodCaller(BaseCaller):
    """"""

    def __init__(
            self,
            domain: Text,
            auth_token: Text,
            is_webhook: bool,
            api_method: Text,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
            bitrix_token: Optional["BitrixTokenProtocol"] = None,
            **kwargs,
    ):
        super().__init__(
            domain=domain,
            auth_token=auth_token,
            is_webhook=is_webhook,
            api_method=api_method,
            params=params,
            timeout=timeout,
            bitrix_token=bitrix_token,
            **kwargs,
        )

    @property
    def _dynamic_auth_token(self) -> Text:
        """"""
        return ("", f"{self._auth_token}/")[self._is_webhook]

    @property
    def _url(self) -> Text:
        """"""
        return f"https://{self._domain}/rest/{self._dynamic_auth_token}{self._api_method}.json"

    @property
    def _dynamic_params(self) -> JSONDict:
        """"""
        if self._is_webhook:
            return self._params
        else:
            return self._params | {"auth": self._auth_token}

    def call(self) -> JSONDict:
        """"""
        self._config.logger.debug(
            "start call_method",
            context=dict(
                domain=self._domain,
                method=self._api_method,
                parameters=self._params,
            ),
        )
        json_response = call(
                url=self._url,
                params=self._dynamic_params,
                timeout=self._timeout,
                **self._kwargs,
        )
        self._config.logger.debug(
            "finish call_method",
            context=dict(
                result=json_response["result"],
                time=json_response["time"],
            ),
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
        bitrix_token: Optional["BitrixTokenProtocol"] = None,
        **kwargs,
) -> JSONDict:
    """
    Call a Bitrix API method

    Args:
        domain: bitrix portal domain
        auth_token: auth token
        is_webhook: whether the method is being called using webhook token
        api_method: name of the bitrix API method to call, e.g. crm.deal.add
        params: API method parameters
        timeout: timeout in seconds
        bitrix_token:

    Returns:
        dictionary containing the result of the API method call and information about call time
    """
    return _MethodCaller(
        domain=domain,
        auth_token=auth_token,
        is_webhook=is_webhook,
        api_method=api_method,
        params=params,
        timeout=timeout,
        bitrix_token=bitrix_token,
        **kwargs,
    ).call()
