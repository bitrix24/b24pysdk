from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONList, Timeout
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
            skip_external: Optional[Union[bool, B24BoolStrict]] = MISSING,
            skip_external_except_types: Optional[Text] = MISSING,
            limit: Optional[int] = MISSING,
            last_id: Optional[int] = MISSING,
            offset: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONList]:
        """"""

        params = dict(
            DIALOG_ID=dialog_id,
        )

        if skip_external is not MISSING:
            params["SKIP_EXTERNAL"] = B24BoolStrict(skip_external).to_b24()

        if skip_external_except_types is not MISSING:
            params["SKIP_EXTERNAL_EXCEPT_TYPES"] = skip_external_except_types

        if limit is not MISSING:
            params["LIMIT"] = limit

        if last_id is not MISSING:
            params["LAST_ID"] = last_id

        if offset is not MISSING:
            params["OFFSET"] = offset

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )
