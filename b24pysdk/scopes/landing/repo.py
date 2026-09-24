from typing import Optional, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Repo",
]


class Repo(BaseEntity):
    """Methods for working with custom blocks.

    Documentation: https://apidocs.bitrix24.com/api-reference/landing/user-blocks/index.html
    """

    @type_checker
    def register(
            self,
            code: Text,
            fields: JSONDict,
            *,
            manifest: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a custom nlock to repository

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/user-blocks/landing-repo-register.html

        The method adds a new custom block to the repository.

        Args:
            code: Unique block code;

            fields: Block fields;

            manifest: Block manifest;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "code": code,
            "fields": fields,
        }

        if manifest is not MISSING:
            params["manifest"] = manifest

        return self._make_bitrix_api_request(
            api_wrapper=self.register,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unregister(
            self,
            code: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete user block

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/user-blocks/landing-repo-unregister.html

        The method deletes a user block by its code.

        Args:
            code: Unique block code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unregister,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def bind(
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
            api_wrapper=self.bind,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unbind(
            self,
            code: Text,
            *,
            handler: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """"""

        params: JSONDict = {
            "code": code,
        }

        if handler is not MISSING:
            params["handler"] = handler

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            params: Optional[JSONDict] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of custom blocks

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/user-blocks/landing-repo-get-list.html

        The method retrieves a list of custom blocks.

        Args:
            params: Object format:

                {
                    select: value_1,

                    filter: value_2,

                    order: value_3,

                    group: value_4,

                    limit: value_5,

                    offset: value_6
                },

                where value_n — value of the corresponding selection parameter;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        _params: JSONDict = {}

        if params is not MISSING:
            _params["params"] = params

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=_params or None,
            timeout=timeout,
        )

    @type_checker
    def check_content(
            self,
            content: Text,
            *,
            splitter: Optional[Text] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Check content for dangerous substrings

        Documentation: https://apidocs.bitrix24.com/api-reference/landing/user-blocks/landing-repo-check-content.html

        The method checks content through a sanitizer.

        Args:
            content: Content to be checked;

            splitter: A delimiter that marks dangerous fragments in content;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "content": content,
        }

        if splitter is not MISSING:
            params["splitter"] = splitter

        return self._make_bitrix_api_request(
            api_wrapper=self.check_content,
            params=params,
            timeout=timeout,
        )
