from abc import ABC, abstractmethod
from typing import Generic, Optional, Text, TypeVar

from ...protocols import BitrixTokenFullProtocol
from ...utils.types import B24RequestTuple, JSONDict

__all__ = [
    "AbstractBitrixAPIRequest",
]

_BARPT = TypeVar("_BARPT")


class AbstractBitrixAPIRequest(ABC, Generic[_BARPT]):
    """"""

    __slots__ = ("_api_method", "_bitrix_token", "_kwargs", "_params", "_response")

    _bitrix_token: BitrixTokenFullProtocol
    _api_method: Text
    _params: Optional[JSONDict]
    _kwargs: JSONDict
    _response: Optional[_BARPT]

    def __init__(
            self,
            *,
            bitrix_token: BitrixTokenFullProtocol,
            api_method: Text,
            params: Optional[JSONDict] = None,
            **kwargs: JSONDict,
    ):
        self._bitrix_token = bitrix_token
        self._api_method = api_method
        self._params = params
        self._kwargs = kwargs
        self._response = None

    def __str__(self):
        return f"<{self.__class__.__name__} {self._api_method}({self._param_string})>"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"bitrix_token={self._bitrix_token}, "
            f"api_method='{self._api_method}', "
            f"params={self._params})"
        )

    @property
    def _param_string(self) -> Text:
        """"""
        if isinstance(self._params, dict):
            return ", ".join(f"{key}={value}" for key, value in self._params.items())
        else:
            return ""

    @property
    def _as_tuple(self) -> B24RequestTuple:
        """"""
        return self._api_method, self._params

    @property
    def response(self) -> _BARPT:
        """"""
        return self._response or self._get_and_set_response()

    def _call(self) -> JSONDict:
        """"""
        return self._bitrix_token.call_method(
            api_method=self._api_method,
            params=self._params,
            **self._kwargs,
        )

    @staticmethod
    @abstractmethod
    def _convert_response(response: JSONDict) -> _BARPT:
        """"""
        raise NotImplementedError

    def _get_and_set_response(self) -> _BARPT:
        """"""
        self._response = self._convert_response(self._call())
        return self._response

    def call(self) -> _BARPT:
        """"""
        return self._get_and_set_response()
