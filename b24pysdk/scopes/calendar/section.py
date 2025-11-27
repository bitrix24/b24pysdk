from typing import Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Section",
]


class Section(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            type: Text,
            owner_id: int,
            name: Text,
            *,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            text_color: Optional[Text] = None,
            export: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
            "name": name,
        }

        if description is not None:
            params["description"] = description

        if color is not None:
            params["color"] = color

        if text_color is not None:
            params["text_color"] = text_color

        if export is not None:
            params["export"] = export

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            type: Text,
            owner_id: int,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            type: Text,
            owner_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            type: Text,
            owner_id: int,
            bitrix_id: Text,
            *,
            name: Optional[Text] = None,
            description: Optional[Text] = None,
            color: Optional[Text] = None,
            text_color: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "type": type,
            "ownerId": owner_id,
            "id": bitrix_id,
        }

        if name is not None:
            params["name"] = name

        if description is not None:
            params["description"] = description

        if color is not None:
            params["color"] = color

        if text_color is not None:
            params["text_color"] = text_color

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

