from typing import Iterable, Optional, Text

from ...._constants import MISSING
from ....api.requests import BitrixAPIRequest
from ....utils.functional import classproperty, type_checker
from ....utils.types import JSONDict, Timeout
from ..._base_entity import BaseEntity

__all__ = [
    "Document",
]


class Document(BaseEntity):
    """Handle custom fields for inventory accounting documents.

    Documentation: https://apidocs.bitrix24.com/api-reference/catalog/userfield-document/index.html
    """

    @classproperty
    def _name(cls) -> Text:
        return "document"

    @type_checker
    def list(
            self,
            select: Iterable[Text],
            filter: JSONDict,
            *,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        if select.__class__ is not list:
            select = list(select)

        params: JSONDict = {
            "select": select,
            "filter": filter,
        }

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            document_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update user field values

        Documentation: https://apidocs.bitrix24.com/api-reference/catalog/userfield-document/catalog-userfield-document-update.html

        The method updates the values of user fields in inventory accounting documents.

        Args:
            document_id: Identifier of the inventory accounting document;

            fields: Fields to be updated;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {
            "documentId": document_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
