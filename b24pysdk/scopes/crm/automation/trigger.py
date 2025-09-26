from typing import TYPE_CHECKING, Optional, Text

from ....bitrix_api.classes import BitrixAPIRequest
from ....utils.functional import type_checker
from ....utils.types import Timeout
from ..base_crm import BaseCRM

if TYPE_CHECKING:
    from .automation import Automation


class Trigger(BaseCRM):
    """The class provide methods for working with application triggers.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/automation/triggers/index.html
    """

    def __init__(self, automation: "Automation"):
        super().__init__(automation._scope)
        self._path = self._get_path(automation)

    @type_checker
    def __call__(
            self,
            *,
            target: Text,
            code: Optional[Text] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Activate trigger.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automation/crm-automation-trigger.html

        The method activates the webhook trigger configured in CRM automation.

        Args:
            target: Target object for automation, specified in the form of TYPENAME_ID;

            code: Unique symbolic code of the trigger configured in Automation for a specific statux\stage of the document;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "target": target,
        }

        if code is not None:
            params["code"] = code

        return self._make_bitrix_api_request(
            api_method=self,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def add(
            self,
            *,
            code: Text,
            name: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add trigger.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automation/triggers/crm-automation-trigger-add.html

        The method adds a trigger.

        Args:
            code: Internal unique identifier of the trigger;

            name: Name of the trigger;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CODE": code,
            "name": name,
        }

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def execute(
            self,
            *,
            code: Text,
            owner_type_id: int,
            owner_id: int,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Executes the trigger.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automation/triggers/crm-automation-trigger-execute.html

        The method triggers the execution of a trigger.

        Args:
            code: Internal unique identifier of the trigger;

            owner_type_id: Type of the CRM object;

            owner_id: Identifier of the entity;

            timeout: Timeout in seconds.

        Returns:
            Instance on BitrixAPIRequest
        """

        params = {
            "CODE": code,
            "OWNER_TYPE_ID": owner_type_id,
            "OWNER_ID": owner_id,
        }

        return self._make_bitrix_api_request(
            api_method=self.execute,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of triggers.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automation/triggers/crm-automation-trigger-list.html

        The method retrieves a list of application triggers.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return self._list(timeout=timeout)

    @type_checker
    def delete(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete triggers.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/automation/triggers/crm-automation-trigger-delete.html

        The method deletes a trigger.

        Args:
            code: Internal unique identifier of the trigger;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "CODE": code,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
