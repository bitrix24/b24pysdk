from typing import Optional, TYPE_CHECKING

from ...._bitrix_api_request import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict

from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .timeline import Timeline


class Bindings(BaseCRM):
    """The methods provide capabilities for managing bindings between timeline records and CRM entities.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/index.html
    """

    def __init__(self, timeline: "Timeline"):
        super().__init__(scope=timeline._scope)
        self._path = self._get_path(timeline)

    def fields(
            self,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get CRM entity binding fields and timeline record.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/crm-timeline-bindings-fields.html

        This method retrieves a list of available fields for linking CRM entities and timeline records.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().fields(timeout=timeout)

    @type_checker
    def list(
            self,
            filter: JSONDict,
            *,
            timeout: Optional[int] = None,
    ) -> BitrixAPIRequest:
        """Get the list of bindings for a record in the timeline.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/crm-timeline-bindings-list.html

        This method retrieves the list of bindings for a record in the timeline.

        Args:
            filter: Object format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                }, where the OWNER_ID field must be used;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "filter": filter
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.list),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def bind(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ):
        """Add timeline record binding to CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/crm-timeline-bindings-bind.html

        THe method adds a binding of a timeline record to a CRM entity.

        Args:
            fields: Object format:
                {
                    "OWNER_ID": "value",

                    "ENTITY_ID": "value",

                    "ENTITY_TYPE": "value",
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "fields": fields
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.bind),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def unbind(
            self,
            fields: JSONDict,
            *,
            timeout: Optional[int] = None,
    ):
        """Unbind timeline record from CRM entity.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/crm-timeline-bindings-unbind.html

        This method removes the binding of a timeline record from a CRM entity.

        Args:
            fields: Object format:
                {
                    "OWNER_ID": "value",

                    "ENTITY_ID": "value",

                    "ENTITY_TYPE": "value",
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        params = {
            "fields": fields
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.unbind),
            params=params,
            timeout=timeout,
        )
