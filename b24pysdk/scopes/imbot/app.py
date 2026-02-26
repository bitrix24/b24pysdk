from typing import Iterable, Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "App",
]


class App(BaseEntity):
    """"""

    @type_checker
    def register(  # noqa: C901, PLR0912
            self,
            bot_id: int,
            code: Text,
            *,
            js_method: Optional[Text] = None,
            js_param: Optional[Text] = None,
            icon_file: Optional[Text] = None,
            context: Optional[Text] = None,
            extranet_support: Optional[Text] = None,
            livechat_support: Optional[Text] = None,
            iframe_popup: Optional[Text] = None,
            lang: Optional[Iterable[JSONDict]] = None,
            iframe: Optional[Text] = None,
            iframe_width: Optional[Text] = None,
            iframe_height: Optional[Text] = None,
            hash: Optional[Text] = None,
            hidden: Optional[Text] = None,
            copyright: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["BOT_ID"] = bot_id
        params["CODE"] = code

        if js_method is not None:
            params["JS_METHOD"] = js_method

        if js_param is not None:
            params["JS_PARAM"] = js_param

        if icon_file is not None:
            params["ICON_FILE"] = icon_file

        if context is not None:
            params["CONTEXT"] = context

        if extranet_support is not None:
            params["EXTRANET_SUPPORT"] = extranet_support

        if livechat_support is not None:
            params["LIVECHAT_SUPPORT"] = livechat_support

        if iframe_popup is not None:
            params["IFRAME_POPUP"] = iframe_popup

        if lang is not None:
            if lang.__class__ is not list:
                lang = list(lang)

            params["LANG"] = lang

        if iframe is not None:
            params["IFRAME"] = iframe

        if iframe_width is not None:
            params["IFRAME_WIDTH"] = iframe_width

        if iframe_height is not None:
            params["IFRAME_HEIGHT"] = iframe_height

        if hash is not None:
            params["HASH"] = hash

        if hidden is not None:
            params["HIDDEN"] = hidden

        if copyright is not None:
            params["COPYRIGHT"] = copyright

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            app_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = dict()
        params["APP_ID"] = app_id

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )
