from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Landing",
]


class Landing(BaseEntity):
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
    def add_by_template(
            self,
            site_id: int,
            code: Text,
            *,
            fields: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "siteId": site_id,
            "code": code,
        }

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.add_by_template,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def addblock(
            self,
            lid: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def copy(
            self,
            lid: int,
            *,
            to_site_id: Optional[int] = None,
            to_folder_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "lid": lid,
        }

        if to_site_id is not None:
            params["toSiteId"] = to_site_id

        if to_folder_id is not None:
            params["toFolderId"] = to_folder_id

        return self._make_bitrix_api_request(
            api_wrapper=self.copy,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def copyblock(
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
            api_wrapper=self.copyblock,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def deleteblock(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.deleteblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def downblock(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.downblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def favorite_block(
            self,
            lid: int,
            block: int,
            *,
            meta: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        if meta is not None:
            params["meta"] = meta

        return self._make_bitrix_api_request(
            api_wrapper=self.favorite_block,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def getadditionalfields(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getadditionalfields,
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
    def getpreview(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getpreview,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getpublicurl(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.getpublicurl,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def hideblock(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.hideblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_delete(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_deleted_block(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_deleted_block,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_un_delete(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_un_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_undeleted_block(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_undeleted_block,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            lid: int,
            *,
            to_site_id: Optional[int] = None,
            to_folder_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "lid": lid,
        }

        if to_site_id is not None:
            params["toSiteId"] = to_site_id

        if to_folder_id is not None:
            params["toFolderId"] = to_folder_id

        return self._make_bitrix_api_request(
            api_wrapper=self.move,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def moveblock(
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
            api_wrapper=self.moveblock,
            params=api_params or None,
            timeout=timeout,
        )

    @type_checker
    def publication(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.publication,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def remove_entities(
            self,
            lid: int,
            data: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.remove_entities,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def resolve_id_by_public_url(
            self,
            landing_url: Text,
            site_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "landingUrl": landing_url,
            "siteId": site_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.resolve_id_by_public_url,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def showblock(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.showblock,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def un_favorite_block(
            self,
            block_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "blockId": block_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.un_favorite_block,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unpublic(
            self,
            lid: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unpublic,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            lid: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def upblock(
            self,
            lid: int,
            block: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "lid": lid,
            "block": block,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.upblock,
            params=params,
            timeout=timeout,
        )
