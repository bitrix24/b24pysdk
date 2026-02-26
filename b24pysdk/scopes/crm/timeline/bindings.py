from ....api.requests import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import JSONDict, Timeout
from .._base_crm import BaseCRM

__all__ = [
    "Bindings",
]


class Bindings(BaseCRM):
    """The methods provide capabilities for managing bindings between timeline records and CRM entities.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/index.html
    """

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get CRM entity binding fields and timeline record.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/bindings/crm-timeline-bindings-fields.html

        This method retrieves a list of available fields for linking CRM entities and timeline records.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            filter: JSONDict,
            timeout: Timeout = None,
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
            "filter": filter,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def bind(
            self,
            fields: JSONDict,
            *,
            timeout: Timeout = None,
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
            fields: JSONDict,
            *,
            timeout: Timeout = None,
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
            "fields": fields,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.unbind,
            params=params,
            timeout=timeout,
        )
