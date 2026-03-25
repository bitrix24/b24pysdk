from typing import Iterable, Optional, Text, Union

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Block",
]


class Block(BaseEntity):
    """"""

    @type_checker
    def addcard(
            self,
            lid: int,
            block: int,
            selector: Text,
            content: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "selector": selector,
            "content": content,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addcard,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def change_anchor(
            self,
            lid: int,
            block: int,
            data: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.change_anchor,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def change_node_name(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.change_node_name,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_content_from_repository(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_content_from_repository,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def getbyid(
            self,
            block: int,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "block": block,
        }

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getbyid,
            params=api_params,
            timeout=timeout,
        )

    @type_checker
    def getcontent(
            self,
            lid: int,
            block: int,
            *,
            edit_mode: Optional[int] = None,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if edit_mode is not None:
            api_params["editMode"] = edit_mode

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getcontent,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getlist(
            self,
            lid: Union[int, Iterable[int]],
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if lid.__class__ is not list and lid.__class__ is not int:
            lid = list(lid)

        api_params: JSONDict = {
            "lid": lid,
        }

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getmanifest(
            self,
            lid: int,
            block: int,
            *,
            params: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if params is not None:
            api_params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.getmanifest,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getmanifestfile(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getmanifestfile,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def getrepository(
            self,
            *,
            section: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        api_params: JSONDict = {}

        if section is not None:
            api_params["section"] = section

        return self._make_bitrix_api_request(
            api_wrapper=self.getrepository,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def removecard(
            self,
            lid: int,
            block: int,
            selector: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "selector": selector,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.removecard,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update_cards(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update_cards,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def updateattrs(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.updateattrs,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def updatecontent(
            self,
            lid: int,
            block: int,
            content: Text,
            *,
            designed: Optional[bool] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "content": content,
        }

        if designed is not None:
            params["designed"] = designed

        return self._make_bitrix_api_request(
            api_wrapper=self.updatecontent,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def updatenodes(
            self,
            lid: int,
            block: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.updatenodes,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def uploadfile(
            self,
            block: int,
            picture: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "block": block,
            "picture": picture,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.uploadfile,
            params=params,
            timeout=timeout,
        )
