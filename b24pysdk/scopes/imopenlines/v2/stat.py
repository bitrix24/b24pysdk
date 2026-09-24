from typing import Iterable, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Stat",
]


class Stat(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "Stat"

    @type_checker
    def get(
            self,
            date_from: Text,
            date_to: Text,
            *,
            config_id: int = MISSING,
            config_id_list: Iterable[int] = MISSING,
            source: Text = MISSING,
            source_list: Iterable[Text] = MISSING,
            operator_id: int = MISSING,
            operator_id_list: Iterable[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "dateFrom": date_from,
            "dateTo": date_to,
        }

        if config_id is not MISSING:
            params["configId"] = config_id

        if config_id_list is not MISSING:
            if config_id_list.__class__ is not list:
                config_id_list = list(config_id_list)

            params["configIdList"] = config_id_list

        if source is not MISSING:
            params["source"] = source

        if source_list is not MISSING:
            if source_list.__class__ is not list:
                source_list = list(source_list)

            params["sourceList"] = source_list

        if operator_id is not MISSING:
            params["operatorId"] = operator_id

        if operator_id_list is not MISSING:
            if operator_id_list.__class__ is not list:
                operator_id_list = list(operator_id_list)

            params["operatorIdList"] = operator_id_list

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )
