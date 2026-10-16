from typing import Iterable, Literal, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.converters import bool_to_bitrix
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Operator",
]


class Operator(BaseEntity):
    """Class for retrieves operator ctatuses and load.

    Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/statistics/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "Operator"

    @type_checker
    def list(  # noqa: C901
            self,
            *,
            config_id: int = MISSING,
            config_id_list: Iterable[int] = MISSING,
            user_id: int = MISSING,
            user_id_list: Iterable[int] = MISSING,
            status: Literal["online", "offline", "pause"] = MISSING,
            has_free_slots: bool = MISSING,
            offset: int = MISSING,
            limit: int = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get operators with load

        Documentation: https://apidocs.bitrix24.com/api-reference/imopenlines/statistics/imopenlines-v2-operator-list.html

        The method retrieves operators with their current status and load.

        Args:
            config_id: Open channel ID;

            config_id_list: List of open channel IDs;

            user_id: Operator ID;

            user_id_list: List of operator IDs;

            status: Operator status;

            has_free_slots: Filter by available free slots;

            offset: Pagination offset;

            limit: Page size;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {}

        if config_id is not MISSING:
            params["configId"] = config_id

        if config_id_list is not MISSING:
            if config_id_list.__class__ is not list:
                config_id_list = list(config_id_list)

            params["configIdList"] = config_id_list

        if user_id is not MISSING:
            params["userId"] = user_id

        if user_id_list is not MISSING:
            if user_id_list.__class__ is not list:
                user_id_list = list(user_id_list)

            params["userIdList"] = user_id_list

        if status is not MISSING:
            params["status"] = status

        if has_free_slots is not MISSING:
            params["hasFreeSlots"] = bool_to_bitrix(has_free_slots, is_required=True)

        if offset is not MISSING:
            params["offset"] = offset

        if limit is not MISSING:
            params["limit"] = limit

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params or None,
            timeout=timeout,
        )
