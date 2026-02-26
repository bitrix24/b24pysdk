from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "AttachedVote",
]


class AttachedVote(BaseEntity):
    """"""

    @type_checker
    def download(
            self,
            *,
            attach_id: Optional[int] = None,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if attach_id is not None:
            params["attachId"] = attach_id

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.download,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            attach_id: int,
            *,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
        }

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_answer_voted(
            self,
            attach_id: int,
            answer_id: int,
            *,
            page_navigation: Optional[JSONDict] = None,
            user_for_mobile_format: Optional[bool] = None,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
            "answerId": answer_id,
        }

        if page_navigation is not None:
            params["pageNavigation"] = page_navigation

        if user_for_mobile_format is not None:
            params["userForMobileFormat"] = user_for_mobile_format

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_answer_voted,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_many(
            self,
            module_id: Text,
            entity_type: Text,
            entity_ids: Iterable[int],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if entity_ids.__class__ is not list:
            entity_ids = list(entity_ids)

        params = {
            "moduleId": module_id,
            "entityType": entity_type,
            "entityIds": entity_ids,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_many,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_with_voted(
            self,
            attach_id: int,
            *,
            page_size: Optional[int] = None,
            user_for_mobile_format: Optional[bool] = None,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
        }

        if page_size is not None:
            params["pageSize"] = page_size

        if user_for_mobile_format is not None:
            params["userForMobileFormat"] = user_for_mobile_format

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_with_voted,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def recall(
            self,
            attach_id: int,
            *,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
        }

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.recall,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def resume(
            self,
            attach_id: int,
            *,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
        }

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.resume,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def stop(
            self,
            attach_id: int,
            *,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
        }

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.stop,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def vote(
            self,
            attach_id: int,
            ballot: JSONDict,
            *,
            module_id: Optional[Text] = None,
            entity_type: Optional[Text] = None,
            entity_id: Optional[int] = None,
            signed_attach_id: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "attachId": attach_id,
            "ballot": ballot,
        }

        if module_id is not None:
            params["moduleId"] = module_id

        if entity_type is not None:
            params["entityType"] = entity_type

        if entity_id is not None:
            params["entityId"] = entity_id

        if signed_attach_id is not None:
            params["signedAttachId"] = signed_attach_id

        return self._make_bitrix_api_request(
            api_wrapper=self.vote,
            params=params,
            timeout=timeout,
        )
