from typing import Iterable, Optional, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24Bool, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Folder",
]


class Folder(BaseEntity):
    """"""

    @type_checker
    def addsubfolder(
            self,
            bitrix_id: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addsubfolder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def copyto(
            self,
            bitrix_id: int,
            target_folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "targetFolderId": target_folder_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.copyto,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def deletetree(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.deletetree,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_external_link(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_external_link,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getchildren(
            self,
            bitrix_id: int,
            *,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        if filter is not None:
            params["filter"] = filter

        if start is not None:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.getchildren,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getfields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

    @type_checker
    def markdeleted(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.markdeleted,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def moveto(
            self,
            bitrix_id: int,
            target_folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "targetFolderId": target_folder_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.moveto,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def rename(
            self,
            bitrix_id: int,
            new_name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "newName": new_name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.rename,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def restore(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.restore,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def uploadfile(
            self,
            bitrix_id: int,
            file_content: Text,
            data: JSONDict,
            *,
            generate_unique_name: Optional[bool] = None,
            rights: Optional[Iterable[JSONDict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "id": bitrix_id,
            "fileContent": file_content,
            "data": data,
        }

        if generate_unique_name is not None:
            params["generateUniqueName"] = B24Bool(generate_unique_name).to_str()

        if rights is not None:
            if rights.__class__ is not list:
                rights = list(rights)

            params["rights"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.uploadfile,
            params=params,
            timeout=timeout,
        )
