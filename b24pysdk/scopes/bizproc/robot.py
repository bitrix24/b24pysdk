from typing import Optional, Sequence, Text, Union

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24BoolStrict, DocumentType, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Robot",
]


class Robot(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            code: Text,
            handler: Text,
            name: Union[Text, JSONDict],
            *,
            auth_user_id: Optional[int] = None,
            use_subscription: Optional[Union[bool, B24BoolStrict]] = None,
            description: Optional[Union[Text, JSONDict]] = None,
            properties: Optional[JSONDict] = None,
            return_properties: Optional[JSONDict] = None,
            document_type: Optional[Sequence[Text]] = None,
            filter: Optional[JSONDict] = None,
            use_placement: Optional[Union[bool, B24BoolStrict]] = None,
            placement_handler: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
            "HANDLER": handler,
            "NAME": name,
        }

        if auth_user_id is not None:
            params["AUTH_USER_ID"] = auth_user_id

        if use_subscription is not None:
            params["USE_SUBSCRIPTION"] = B24BoolStrict(use_subscription).to_b24()

        if description is not None:
            params["DESCRIPTION"] = description

        if properties is not None:
            params["PROPERTIES"] = properties

        if return_properties is not None:
            params["RETURN_PROPERTIES"] = return_properties

        if document_type is not None:
            params["DOCUMENT_TYPE"] = DocumentType(document_type).to_b24()

        if filter is not None:
            params["FILTER"] = filter

        if use_placement is not None:
            params["USE_PLACEMENT"] = B24BoolStrict(use_placement).to_b24()

        if placement_handler is not None:
            params["PLACEMENT_HANDLER"] = placement_handler

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            code: Text,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
            "FIELDS": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )
