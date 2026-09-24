from typing import Optional

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Stage",
]


class Stage(BaseEntity):
    """Methods for working with stages.

    Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/stage/index.html
    """

    @type_checker
    def add(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Create a new stage

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/stage/rpa-stage-add.html

        This method adds a new stage.

        Args:
            fields: An object with fields of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete stage

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/stage/rpa-stage-delete.html

        This method deletes a stage.

        Args:
            bitrix_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.delete,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about stage

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/stage/rpa-stage-get.html

        This method retrieves information about a stage by its id.

        Args:
            bitrix_id: Identifier of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list_for_type(
            self,
            type_id: int,
            *,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get the list of stages for the process

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/stage/rpa-stage-list-for-type.html

        This method retrieves a list of process stages, sorted on order with final stages at the end.

        Args:
            type_id: Identifier of the process;

            start: The parameter is used for managing pagination;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "typeId": type_id,
        }

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.list_for_type,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update stage

        Documentation: https://apidocs.bitrix24.com/api-reference/outdated/rpa/stage/rpa-stage-update.html

        This method updates the stage by id.

        Args:
            bitrix_id: Identifier of the stage;

            fields: Object with fields of the stage;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params: JSONDict = {
            "id": bitrix_id,
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.update,
            params=params,
            timeout=timeout,
        )
