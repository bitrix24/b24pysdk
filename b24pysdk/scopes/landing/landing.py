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
            *,
            fields: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params or None,
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
    def copy(
            self,
            landing_id: int,
            *,
            to_site_id: Optional[int] = None,
            to_folder_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "lid": landing_id,
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
    def delete(
            self,
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def getadditionalfields(
            self,
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.getadditionalfields,
            params=params or None,
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
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.getpreview,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def getpublicurl(
            self,
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.getpublicurl,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def mark_delete(
            self,
            landing_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "lid": landing_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def mark_un_delete(
            self,
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.mark_un_delete,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def move(
            self,
            landing_id: int,
            *,
            to_site_id: Optional[int] = None,
            to_folder_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "lid": landing_id,
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
    def publication(
            self,
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.publication,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def remove_entities(
            self,
            *,
            landing_id: Optional[int] = None,
            data: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        if data is not None:
            params["data"] = data

        return self._make_bitrix_api_request(
            api_wrapper=self.remove_entities,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def resolve_id_by_public_url(
            self,
            *,
            landing_url: Optional[Text] = None,
            site_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_url is not None:
            params["landingUrl"] = landing_url

        if site_id is not None:
            params["siteId"] = site_id

        return self._make_bitrix_api_request(
            api_wrapper=self.resolve_id_by_public_url,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def unpublic(
            self,
            *,
            landing_id: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unpublic,
            params=params or None,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            *,
            landing_id: Optional[int] = None,
            fields: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()

        if landing_id is not None:
            params["lid"] = landing_id

        if fields is not None:
            params["fields"] = fields

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params or None,
            timeout=timeout,
        )
