from functools import cached_property
from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity
from .list import List
from .path import Path

__all__ = [
    "Config",
]


class Config(BaseEntity):
    """"""

    @cached_property
    def list(self) -> List:
        """"""
        return List(self)

    @cached_property
    def path(self) -> Path:
        """"""
        return Path(self)

    @type_checker
    def add(
            self,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = dict()

        if params is not MISSING:
            payload["PARAMS"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=payload or None,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            config_id: Union[int, Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONFIG_ID=config_id,
        )

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            config_id: Union[int, Text],
            *,
            with_queue: Optional[bool] = MISSING,
            show_offline: Optional[bool] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONFIG_ID=config_id,
        )

        if with_queue is not MISSING:
            params["WITH_QUEUE"] = bool_to_bitrix(with_queue, is_required=True)

        if show_offline is not MISSING:
            params["SHOW_OFFLINE"] = bool_to_bitrix(show_offline, is_required=True)

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            config_id: Union[int, Text],
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = dict(
            CONFIG_ID=config_id,
        )

        if params is not MISSING:
            payload["PARAMS"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=payload,
            timeout=timeout,
        )
