from typing import Optional, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import classproperty, type_checker
from ...utils.types import Timeout
from .._base_entity import BaseEntity

__all__ = [
    "ExternalCall",
]


class ExternalCall(BaseEntity):
    """"""

    @classproperty
    def _name(cls) -> Text:
        return "externalCall"

    @type_checker
    def attach_record(
            self,
            call_id: Text,
            filename: Text,
            *,
            file_content: Optional[Text] = None,
            record_url: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "CALL_ID": call_id,
            "FILENAME": filename,
        }

        if file_content is not None:
            params["FILE_CONTENT"] = file_content

        if record_url is not None:
            params["RECORD_URL"] = record_url

        return self._make_bitrix_api_request(
            api_wrapper=self.attach_record,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def search_crm_entities(
            self,
            phone_number: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params = {
            "PHONE_NUMBER": phone_number,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.search_crm_entities,
            params=params,
            timeout=timeout,
        )
