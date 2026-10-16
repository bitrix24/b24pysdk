from typing import Optional, Text

from .._constants import MISSING
from ..api.requests import BitrixAPIRequest
from ..utils.functional import type_checker
from ..utils.types import JSONDict, Timeout
from ._base_scope import BaseScope

__all__ = [
    "Userfieldtype",
]


class Userfieldtype(BaseScope):
    """Class for managing an application's own custom field types.

    Documentation: https://apidocs.bitrix24.com/api-reference/widgets/user-field/index.html
    """

    @type_checker
    def add(
            self,
            user_type_id: Text,
            handler: Text,
            *,
            title: Optional[Text] = MISSING,
            description: Optional[Text] = MISSING,
            options: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Register a new user fields type

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/user-field/userfieldtype-add.html

        The method registers a new type of user fields.

        Args:
            user_type_id: String type code;

            handler: Custom type handler address;

            title: Textual type name;

            description: Textual type description;

            options: Additional settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "USER_TYPE_ID": user_type_id,
            "HANDLER": handler,
        }

        if title is not MISSING:
            params["TITLE"] = title

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if options is not MISSING:
            params["OPTIONS"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            user_type_id: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Delete registered user field type

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/user-field/userfieldtype-delete.html

        The method removes a user field type registered by the application.

        Args:
            user_type_id: String code of the type;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "USER_TYPE_ID": user_type_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[JSONDict]:
        """Get a list of registered user field types

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/user-field/userfieldtype-list.html

        The method retrieves a list of user fields types registered by the application.

        Args:
            start: Offset for pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params: JSONDict = {}

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
            user_type_id: Text,
            handler: Text,
            title: Text,
            *,
            description: Optional[Text] = MISSING,
            options: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest[bool]:
        """Change settings for user field type

        Documentation: https://apidocs.bitrix24.com/api-reference/widgets/user-field/userfieldtype-update.html

        The method modifies settings of a user field type previously registered by the application.

        Args:
            user_type_id: String type code;

            handler: Custom type handler address;

            title: Textual type name;

            description: Textual type description;

            options: Additional settings;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "USER_TYPE_ID": user_type_id,
            "HANDLER": handler,
            "TITLE": title,
        }

        if description is not MISSING:
            params["DESCRIPTION"] = description

        if options is not MISSING:
            params["OPTIONS"] = options

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
