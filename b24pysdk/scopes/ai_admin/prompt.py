from typing import Annotated, Iterable, Literal, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Prompt",
]


class Prompt(BaseEntity):
    """"""

    @type_checker
    def register(
            self,
            code: Text,
            prompt: Text,
            *,
            category: Optional[Iterable[Text]] = None,
            icon: Optional[Text] = None,
            parent_code: Optional[Text] = None,
            section: Optional[Annotated[Text, Literal["create", "edit"]]] = None,
            sort: Optional[int] = None,
            translate: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "code": code,
            "prompt": prompt,
        }

        if category is not None:
            if category.__class__ is not list:
                category = list(category)

            params["category"] = category

        if icon is not None:
            params["icon"] = icon

        if parent_code is not None:
            params["parent_code"] = parent_code

        if section is not None:
            params["section"] = section

        if sort is not None:
            params["sort"] = sort

        if translate is not None:
            params["translate"] = translate

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
