from functools import cached_property
from typing import Optional, Text, Union

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
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
            sort: Optional[JSONDict] = MISSING,
            filter: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
        }

        if sort is not MISSING:
            params["SORT"] = sort

        if filter is not MISSING:
            params["FILTER"] = filter

        if start is not MISSING:
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
            active: Optional[Union[bool, B24BoolStrict]] = MISSING,
            date_active_from: Optional[Text] = MISSING,
            date_active_to: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            preview_picture: Optional[JSONDict] = MISSING,
            preview_text: Optional[Text] = MISSING,
            detail_picture: Optional[JSONDict] = MISSING,
            detail_text: Optional[Text] = MISSING,
            code: Optional[Text] = MISSING,
            section: Optional[int] = MISSING,
            property_values: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "NAME": name,
        }

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if date_active_from is not MISSING:
            params["DATE_ACTIVE_FROM"] = date_active_from

        if date_active_to is not MISSING:
            params["DATE_ACTIVE_TO"] = date_active_to

        if sort is not MISSING:
            params["SORT"] = sort

        if preview_picture is not MISSING:
            params["PREVIEW_PICTURE"] = preview_picture

        if preview_text is not MISSING:
            params["PREVIEW_TEXT"] = preview_text

        if detail_picture is not MISSING:
            params["DETAIL_PICTURE"] = detail_picture

        if detail_text is not MISSING:
            params["DETAIL_TEXT"] = detail_text

        if code is not MISSING:
            params["CODE"] = code

        if section is not MISSING:
            params["SECTION"] = section

        if property_values is not MISSING:
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
            name: Optional[Text] = MISSING,
            active: Optional[Union[bool, B24BoolStrict]] = MISSING,
            date_active_from: Optional[Text] = MISSING,
            date_active_to: Optional[Text] = MISSING,
            sort: Optional[int] = MISSING,
            preview_picture: Optional[JSONDict] = MISSING,
            preview_text: Optional[Text] = MISSING,
            detail_picture: Optional[JSONDict] = MISSING,
            detail_text: Optional[Text] = MISSING,
            code: Optional[Text] = MISSING,
            section: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "ENTITY": entity,
            "ID": bitrix_id,
            "PROPERTY_VALUES": property_values,
        }

        if name is not MISSING:
            params["NAME"] = name

        if active is not MISSING:
            params["ACTIVE"] = B24BoolStrict(active).to_b24()

        if date_active_from is not MISSING:
            params["DATE_ACTIVE_FROM"] = date_active_from

        if date_active_to is not MISSING:
            params["DATE_ACTIVE_TO"] = date_active_to

        if sort is not MISSING:
            params["SORT"] = sort

        if preview_picture is not MISSING:
            params["PREVIEW_PICTURE"] = preview_picture

        if preview_text is not MISSING:
            params["PREVIEW_TEXT"] = preview_text

        if detail_picture is not MISSING:
            params["DETAIL_PICTURE"] = detail_picture

        if detail_text is not MISSING:
            params["DETAIL_TEXT"] = detail_text

        if code is not MISSING:
            params["CODE"] = code

        if section is not MISSING:
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
