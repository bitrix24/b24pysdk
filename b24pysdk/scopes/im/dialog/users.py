from typing import Optional, Text, Union

from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Users",
]


class Users(BaseEntity):
    """"""

    @type_checker
    def list(
            self,
            dialog_id: Text,
            *,
            skip_external: Optional[Union[bool, B24BoolStrict]] = None,
            skip_external_except_types: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if skip_external is not None:
            params["SKIP_EXTERNAL"] = B24BoolStrict(skip_external).to_b24()

        if skip_external_except_types is not None:
            params["SKIP_EXTERNAL_EXCEPT_TYPES"] = skip_external_except_types

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
