from typing import TYPE_CHECKING

from ......bitrix_api.classes import BitrixAPIRequest
from ......utils.functional import type_checker
from ......utils.types import JSONDict, Timeout
from ....base_crm import BaseCRM

if TYPE_CHECKING:
    from .preset import Preset


class Field(BaseCRM):
    """The methods provide capabilities for working with custom fields in the requisite template.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/index.html
    """

    def __init__(self, preset: "Preset"):
        super().__init__(preset._scope)
        self._path = self._get_path(preset)

    @type_checker
    def fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get description of custom fields for the CRM requisite template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-fields.html

        This method returns a formal description of the fields that define the customizable field of the requisite template.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._fields(timeout=timeout)

    @type_checker
    def add(
            self,
            *,
            preset: JSONDict,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add a custom field to the CRM requisite template

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-add.html

        This method adds a custom field to the requisite template.
        Before adding a user-defined field to the template it must be created.

        Args:
            preset: An object containing the identifier of the template to which the custom field is being added;

            fields: Object in the format:

                {
                    field_1: value_1,

                    field_2: value_2,

                    ...,

                    field_n: value_n,
                };

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "preset": preset,
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.add),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            bitrix_id: int,
            *,
            preset: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get custom field of requisite template by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-get.html

        This method returns the description of a custom field of the requisite template by its identifier.

        Args:
            bitrix_id: Identifier of the custom field;

            preset: An object containing the identifier of the template from which the information about the custom field is extracted;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "preset": preset,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.get),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            preset: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of customizable fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-list.html

        The method returns a list of all customizable fields for a specific requisites templates.

        Args:
            preset: An object containing the identifier value of the template from which the list of customizable fields is expected;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "preset": preset,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.list),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def update(
            self,
            bitrix_id: int,
            *,
            preset: JSONDict,
            fields: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Update custom fields of a given CRM requisite template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-update.html

        This method updates a custom field in the requisite template.

        Args:
            bitrix_id: Identifier of the custom field to be updated;

            preset: An object containing the identifier of the template to which the custom field is added;

            fields: Object format:

                {

                    "FIELD_NAME": "value",

                    "FIELD_TITLE": "value",

                    "SORT": value,

                    "IN_SHORT_LIST": "value",

                }

                where FIELD_NAME is required;

            timeout: Timeout in seconds.

        Returns:
             Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "preset": preset,
            "fields": fields,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.update),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def delete(
            self,
            bitrix_id: int,
            *,
            preset: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete custom field from CRM requisite template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-delete.html

        This method removes a custom field from the requisite template.

        Args:
            bitrix_id: Identifier of the custom field to be deleted;

            preset: An object containing the identifier of the template from which the custom field is being removed;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "id": bitrix_id,
            "preset": preset,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.delete),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def availabletoadd(
            self,
            *,
            preset: JSONDict,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get fields available for addition to the CRM requisite template.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/requisites/presets/fields/crm-requisite-preset-field-available-to-add.html

        This method returns the fields that can be added to the specified requisite template.

        Args:
            preset: An object containing the identifier value of the template for which you want to get the list of available customizable fields;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "preset": preset,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self.availabletoadd),
            params=params,
            timeout=timeout,
        )
