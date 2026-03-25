from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Site",
]


class Site(BaseEntity):
    """"""

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params = dict()

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def get_preview(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_preview,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_public_url(
            self,
            bitrix_id: Union[int, Iterable[int]],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if bitrix_id.__class__ is not list and not isinstance(bitrix_id, int):
            bitrix_id = list(bitrix_id)

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_public_url,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_un_delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_un_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def publication(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.publication,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpublic(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unpublic,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def set_rights(
            self,
            bitrix_id: int,
            rights: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "rights": rights,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.set_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_rights(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_rights,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getadditionalfields(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getadditionalfields,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add_folder(
            self,
            site_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "siteId": site_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_folders(
            self,
            site_id: int,
            *,
            filter: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "siteId": site_id,
        }

        if filter is not None:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_folders,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def publication_folder(
            self,
            folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "folderId": folder_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.publication_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def un_public_folder(
            self,
            folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "folderId": folder_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.un_public_folder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_folder_delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_folder_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_folder_un_delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_folder_un_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def binding_to_menu(
            self,
            bitrix_id: int,
            menu_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "menuCode": menu_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.binding_to_menu,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def unbinding_from_menu(
            self,
            bitrix_id: int,
            menu_code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "menuCode": menu_code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unbinding_from_menu,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def binding_to_group(
            self,
            bitrix_id: int,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "groupId": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.binding_to_group,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def unbinding_from_group(
            self,
            bitrix_id: int,
            group_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "id": bitrix_id,
            "groupId": group_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unbinding_from_group,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_menu_bindings(
            self,
            *,
            menu_code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if menu_code is not None:
            params["menuCode"] = menu_code

        return self._make_bitrix_api_request(
            api_wrapper=self.get_menu_bindings,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def get_group_bindings(
            self,
            *,
            group_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if group_id is not None:
            params["groupId"] = group_id

        return self._make_bitrix_api_request(
            api_wrapper=self.get_group_bindings,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def full_export(
            self,
            bitrix_id: int,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "id": bitrix_id,
        }

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.full_export,
            params=api_params,
            timeout=timeout,
        )
