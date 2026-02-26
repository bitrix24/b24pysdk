from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import B24Bool, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ExternalLine",
]


class ExternalLine(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "externalLine"

    @type_checker
    def add(
            self,
            number: Text,
            *,
            name: Optional[Text] = None,
            crm_auto_create: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "NUMBER": number,
        }

        if name is not None:
            params["NAME"] = name

        if crm_auto_create is not None:
            params["CRM_AUTO_CREATE"] = B24Bool(crm_auto_create).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            *,
            number: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if number is not None:
            params["NUMBER"] = number

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            *,
            number: Optional[Text] = None,
            name: Optional[Text] = None,
            crm_auto_create: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if number is not None:
            params["NUMBER"] = number

        if name is not None:
            params["NAME"] = name

        if crm_auto_create is not None:
            params["CRM_AUTO_CREATE"] = B24Bool(crm_auto_create).to_b24()

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params or None,
            timeout=timeout,
        )
