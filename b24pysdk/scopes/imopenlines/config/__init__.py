from functools import cached_property
from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .list import List
from .path import Path

__all__ = [
    "Config",
]


class Config(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = dict()

        if params is not None:
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
            with_queue: Optional[Union[bool, B24BoolStrict]] = None,
            show_offline: Optional[Union[bool, B24BoolStrict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            CONFIG_ID=config_id,
        )

        if with_queue is not None:
            params["WITH_QUEUE"] = B24BoolStrict(with_queue).to_b24()

        if show_offline is not None:
            params["SHOW_OFFLINE"] = B24BoolStrict(show_offline).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @cached_property
    def list(self) -> List:
        """"""
        return List(self)

    @cached_property
    def path(self) -> Path:
        """"""
        return Path(self)

    @type_checker
    def update(
            self,
            config_id: Union[int, Text],
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        payload = dict(
            CONFIG_ID=config_id,
        )

        if params is not None:
            payload["PARAMS"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=payload,
            timeout=timeout,
        )
