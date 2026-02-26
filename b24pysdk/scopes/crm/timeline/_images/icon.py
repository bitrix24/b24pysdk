from typing import Text

from .....api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ._base_image import BaseImage

__all__ = [
    "Icon",
]


class Icon(BaseImage):
    """A list of methods for managing log record icons.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/icons/index.html
    """

    @type_checker
    def add(
            self,
            *,
            code: Text,
            file_content: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add icon.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/icons/crm-timeline-icon-add.html

        This method adds a new icon.

        Args:
            code: Icon code;

            file_content: Base64 encoded content of the icon file, where file requirements are:

                - type: png,

                - size: 24x24 pixels,

                - background: transparent;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().add(
            code=code,
            file_content=file_content,
            timeout=timeout,
        )

    @type_checker
    def get(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the icon.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/icons/crm-timeline-icon-get.html

        This method retrieves information about the timeline log entry icon.

        Args:
            code: Icon code;

            timeout: timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().get(code=code, timeout=timeout)

    @type_checker
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available icons.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/icons/crm-timeline-icon-list.html

        This method retrieves a list of available icons for the timeline log entries.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().list(timeout=timeout)

    @type_checker
    def delete(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete icon

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/icons/crm-timeline-icon-delete.html

        This method deletes an icon.

        Args:
            code: Icon code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().delete(code=code, timeout=timeout)
