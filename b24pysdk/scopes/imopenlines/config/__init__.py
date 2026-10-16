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
    """Class for working with open channels.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/index.html
    """

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
        """Add open channel

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-config-add.html

        The method adds a new open channel.

        Args:
            params: Object with open channel settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Delete open channel

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-config-delete.html

        The method removes an open channel.

        Args:
            config_id: Identifier of the open channel;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Get open line by ID

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-config-get.html

        The method retrieves the settings of an open line by its ID.

        Args:
            config_id: Identifier of the open channel;

            with_queue: Return operator queue data;

            show_offline: Return offline operators iin the queue;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
        """Update open channel

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/openlines/imopenlines-config-update.html

        The method updates an open channel.

        Args:
            config_id: Identifier of the open channel;

            params: Object with open channel settings for the update;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

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
