from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Event",
]


class Event(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            command: Text,
            *,
            params: Optional[Iterable[JSONDict]] = MISSING,
            module_id: Optional[Text] = MISSING,
            user_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params = {
            "COMMAND": command,
        }

        if params is not MISSING:
            if params.__class__ is not list:
                params = list(params)

            api_params["PARAMS"] = params

        if module_id is not MISSING:
            api_params["MODULE_ID"] = module_id

        if user_id is not MISSING:
            api_params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=api_params,
            timeout=timeout,
        )
