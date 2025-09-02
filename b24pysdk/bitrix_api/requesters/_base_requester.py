from abc import ABC, abstractmethod
from typing import Dict, Final, Text

from ..._constants import TEXT_PYTHON_VERSION
from ...version import SDK_VERSION


class BaseRequester(ABC):
    """"""

    _SDK_VERSION: Final[Text] = SDK_VERSION
    _SDK_USER_AGENT: Final[Text] = "b24-python-sdk-vendor"
    _TEXT_PYTHON_VERSION: Final[Text] = TEXT_PYTHON_VERSION

    def _get_default_headers(self) -> Dict:
        """"""
        return {
            "Accept": "application/json",
            "Accept-Charset": "utf-8",
            "User-Agent": f"{self._SDK_USER_AGENT}-v-{self._SDK_VERSION}-python-{self._TEXT_PYTHON_VERSION}",
            "X-BITRIX24-PYTHON-SDK-PYTHON-VERSION": self._TEXT_PYTHON_VERSION,
            "X-BITRIX24-PYTHON-SDK-VERSION": self._SDK_VERSION,
        }

    @property
    @abstractmethod
    def _headers(self) -> Dict:
        """"""
        raise NotImplementedError
