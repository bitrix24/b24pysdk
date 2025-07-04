from typing import Text

from ....._bitrix_api_request import BitrixAPIRequest
from .....scopes.crm.timeline.visual_element.visual_element import VisualElement
from .....utils.types import Timeout


class Logo(VisualElement):
    """"""

    def add(
            self,
            code: Text,
            file_content: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return super().add(
            code=code,
            file_content=file_content,
            timeout=timeout,
        )

    def delete(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return super().delete(code=code, timeout=timeout)

    def get(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return super().get(code=code, timeout=timeout)

    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""
        return super().list(timeout=timeout)
