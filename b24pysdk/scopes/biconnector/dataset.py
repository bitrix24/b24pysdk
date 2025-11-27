from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from ._base_biconnector_entity import BaseBiconnectorEntity

__all__ = [
    "Dataset",
]


class Dataset(BaseBiconnectorEntity):
    """"""

    @type_checker
    def fields_update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.fields_update,
            params=params,
            timeout=timeout,
        )
