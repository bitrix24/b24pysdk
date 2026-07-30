from functools import cached_property
from typing import Any, List, Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity
from .getusers import Getusers

__all__ = [
    "Blogpost",
]


class Blogpost(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        """"""
        return "blogpost"

    @cached_property
    def getusers(self) -> Getusers:
        """"""
        return Getusers(self)

    @type_checker
    def add(  # noqa: C901
            self,
            post_message: Text,
            *,
            post_title: Optional[Text] = MISSING,
            dest: Optional[List[Text]] = MISSING,
            sperm: Optional[List[Text]] = MISSING,
            files: Optional[Any] = MISSING,
            important: Optional[Text] = MISSING,
            important_date_end: Optional[Text] = MISSING,
            site_id: Optional[Text] = MISSING,
            user_id: Optional[int] = MISSING,
            tags: Optional[Text] = MISSING,
            background_code: Optional[Text] = MISSING,
            parse_preview: Optional[Text] = MISSING,
            user_fields: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "POST_MESSAGE": post_message,
        }

        if post_title is not MISSING:
            params["POST_TITLE"] = post_title

        if dest is not MISSING:
            params["DEST"] = dest

        if sperm is not MISSING:
            params["SPERM"] = sperm

        if files is not MISSING:
            params["FILES"] = files

        if important is not MISSING:
            params["IMPORTANT"] = important

        if important_date_end is not MISSING:
            params["IMPORTANT_DATE_END"] = important_date_end

        if site_id is not MISSING:
            params["SITE_ID"] = site_id

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if tags is not MISSING:
            params["TAGS"] = tags

        if background_code is not MISSING:
            params["BACKGROUND_CODE"] = background_code

        if parse_preview is not MISSING:
            params["PARSE_PREVIEW"] = parse_preview

        if user_fields is not MISSING:
            params.update(user_fields)

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            post_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "POST_ID": post_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            post_id: Optional[int] = MISSING,
            log_rights: Optional[List[Text]] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {}

        if post_id is not MISSING:
            params["POST_ID"] = post_id

        if log_rights is not MISSING:
            params["LOG_RIGHTS"] = log_rights

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def share(
            self,
            post_id: int,
            dest: List[Text],
            *,
            user_id: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "POST_ID": post_id,
            "DEST": dest,
        }

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        return self._make_bitrix_api_request(
            api_wrapper=self.share,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(  # noqa: C901
            self,
            post_id: int,
            *,
            post_message: Optional[Text] = MISSING,
            post_title: Optional[Text] = MISSING,
            dest: Optional[List[Text]] = MISSING,
            sperm: Optional[List[Text]] = MISSING,
            files: Optional[Any] = MISSING,
            important: Optional[Text] = MISSING,
            important_date_end: Optional[Text] = MISSING,
            site_id: Optional[Text] = MISSING,
            user_id: Optional[int] = MISSING,
            user_fields: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "POST_ID": post_id,
        }

        if post_message is not MISSING:
            params["POST_MESSAGE"] = post_message

        if post_title is not MISSING:
            params["POST_TITLE"] = post_title

        if dest is not MISSING:
            params["DEST"] = dest

        if sperm is not MISSING:
            params["SPERM"] = sperm

        if files is not MISSING:
            params["FILES"] = files

        if important is not MISSING:
            params["IMPORTANT"] = important

        if important_date_end is not MISSING:
            params["IMPORTANT_DATE_END"] = important_date_end

        if site_id is not MISSING:
            params["SITE_ID"] = site_id

        if user_id is not MISSING:
            params["USER_ID"] = user_id

        if user_fields is not MISSING:
            params.update(user_fields)

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
