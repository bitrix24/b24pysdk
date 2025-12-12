from functools import cached_property
from typing import Optional, Text, Union

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24BoolStrict, JSONDict, Timeout
from ..._base_entity import BaseEntity
from .property import Property

__all__ = [
    "Item",
]


class Item(BaseEntity):
    """"""

    @cached_property
    def property(self) -> Property:
        """"""
        return Property(self)

    @type_checker
    def get(
            self,
            entity: Text,
            *,
            sort: Optional[JSONDict] = None,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
        }

        if sort is not None:
            params["SORT"] = sort

        if filter is not None:
            params["FILTER"] = filter

        if start is not None:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(  # noqa: C901
            self,
            entity: Text,
            name: Text,
            *,
            active: Optional[Union[bool, B24BoolStrict]] = None,
            date_active_from: Optional[Text] = None,
            date_active_to: Optional[Text] = None,
            sort: Optional[int] = None,
            preview_picture: Optional[JSONDict] = None,
            preview_text: Optional[Text] = None,
            detail_picture: Optional[JSONDict] = None,
            detail_text: Optional[Text] = None,
            code: Optional[Text] = None,
            section: Optional[int] = None,
            property_values: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "NAME": name,
        }

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if date_active_from is not None:
            params["DATE_ACTIVE_FROM"] = date_active_from

        if date_active_to is not None:
            params["DATE_ACTIVE_TO"] = date_active_to

        if sort is not None:
            params["SORT"] = sort

        if preview_picture is not None:
            params["PREVIEW_PICTURE"] = preview_picture

        if preview_text is not None:
            params["PREVIEW_TEXT"] = preview_text

        if detail_picture is not None:
            params["DETAIL_PICTURE"] = detail_picture

        if detail_text is not None:
            params["DETAIL_TEXT"] = detail_text

        if code is not None:
            params["CODE"] = code

        if section is not None:
            params["SECTION"] = section

        if property_values is not None:
            params["PROPERTY_VALUES"] = property_values

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(  # noqa: C901
            self,
            entity: Text,
            bitrix_id: int,
            property_values: JSONDict,
            *,
            name: Optional[Text] = None,
            active: Optional[Union[bool, B24BoolStrict]] = None,
            date_active_from: Optional[Text] = None,
            date_active_to: Optional[Text] = None,
            sort: Optional[int] = None,
            preview_picture: Optional[JSONDict] = None,
            preview_text: Optional[Text] = None,
            detail_picture: Optional[JSONDict] = None,
            detail_text: Optional[Text] = None,
            code: Optional[Text] = None,
            section: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "ID": bitrix_id,
            "PROPERTY_VALUES": property_values,
        }

        if name is not None:
            params["NAME"] = name

        if active is not None:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if date_active_from is not None:
            params["DATE_ACTIVE_FROM"] = date_active_from

        if date_active_to is not None:
            params["DATE_ACTIVE_TO"] = date_active_to

        if sort is not None:
            params["SORT"] = sort

        if preview_picture is not None:
            params["PREVIEW_PICTURE"] = preview_picture

        if preview_text is not None:
            params["PREVIEW_TEXT"] = preview_text

        if detail_picture is not None:
            params["DETAIL_PICTURE"] = detail_picture

        if detail_text is not None:
            params["DETAIL_TEXT"] = detail_text

        if code is not None:
            params["CODE"] = code

        if section is not None:
            params["SECTION"] = section

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            entity: Text,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "ID": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
