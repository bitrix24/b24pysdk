from functools import cached_property
from typing import Optional, Text

from ....bitrix_api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import B24Bool, JSONDict, Timeout
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
    def add(
            self,
            entity: Text,
            name: Text,
            *,
            active: Optional[bool] = None,
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
        self._apply_common_fields(
            params,
            active=active,
            date_active_from=date_active_from,
            date_active_to=date_active_to,
            sort=sort,
            preview_picture=preview_picture,
            preview_text=preview_text,
            detail_picture=detail_picture,
            detail_text=detail_text,
            code=code,
            section=section,
        )

        if property_values is not None:
            params["PROPERTY_VALUES"] = property_values

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            entity: Text,
            bitrix_id: int,
            property_values: JSONDict,
            *,
            name: Optional[Text] = None,
            active: Optional[bool] = None,
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

        self._apply_common_fields(
            params,
            active=active,
            date_active_from=date_active_from,
            date_active_to=date_active_to,
            sort=sort,
            preview_picture=preview_picture,
            preview_text=preview_text,
            detail_picture=detail_picture,
            detail_text=detail_text,
            code=code,
            section=section,
        )

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

    @staticmethod
    def _apply_common_fields(
            params: JSONDict,
            *,
            active: Optional[bool] = None,
            date_active_from: Optional[Text] = None,
            date_active_to: Optional[Text] = None,
            sort: Optional[int] = None,
            preview_picture: Optional[JSONDict] = None,
            preview_text: Optional[Text] = None,
            detail_picture: Optional[JSONDict] = None,
            detail_text: Optional[Text] = None,
            code: Optional[Text] = None,
            section: Optional[int] = None,
    ) -> None:
        """"""

        mapping = [
            ("ACTIVE", active, lambda value: B24Bool(value).to_str()),
            ("DATE_ACTIVE_FROM", date_active_from, None),
            ("DATE_ACTIVE_TO", date_active_to, None),
            ("SORT", sort, None),
            ("PREVIEW_PICTURE", preview_picture, None),
            ("PREVIEW_TEXT", preview_text, None),
            ("DETAIL_PICTURE", detail_picture, None),
            ("DETAIL_TEXT", detail_text, None),
            ("CODE", code, None),
            ("SECTION", section, None),
        ]

        for key, value, transformer in mapping:
            if value is None:
                continue

            params[key] = transformer(value) if transformer is not None else value

