from typing import TYPE_CHECKING, Text

from .....bitrix_api.classes import BitrixAPIRequest
from .....scopes.crm.base_crm import BaseCRM
from .....utils.functional import type_checker
from .....utils.types import Timeout

if TYPE_CHECKING:
    from b24pysdk.scopes.crm.timeline.timeline import Timeline


class VisualElement(BaseCRM):
    """The class is a base class for logo and icon classes.
    """

    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline._scope)
        self._path = self._get_path(timeline)

    @type_checker
    def add(
            self,
            *,
            code: Text,
            file_content: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add new visual element.

        This method adds a new visual element (logo or icon).

        Args:
            code: Visual element code;

            file_content: Base64 encoded content of the file;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
            "fileContent": file_content,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._add),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the visual element.

        This method retrieves information about the visual element (logo or icon) of the timeline log entry.

        Args:
            code: Visual element code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._get),
            params=params,
            timeout=timeout,
        )

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available visual elements.

        This method retrieves a list of available visual elements (icons or logos) for timeline log entries.

        """
        return self._list(timeout=timeout)

    @type_checker
    def delete(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete visual element.

        This method deletes a visual element.

        Args:
            code: Visual element code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
        }

        return BitrixAPIRequest(
            bitrix_token=self._scope.bitrix_token,
            api_method=self._get_api_method(self._delete),
            params=params,
            timeout=timeout,
        )
