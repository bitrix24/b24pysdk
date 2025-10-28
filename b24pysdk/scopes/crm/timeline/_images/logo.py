from typing import Text

from .....bitrix_api.requests import BitrixAPIRequest
from .....utils.functional import type_checker
from .....utils.types import Timeout
from ._base_image import BaseImage

__all__ = [
    "Logo",
]


class Logo(BaseImage):
    """A list of methods for managing the logos of the entries in the journal.

    Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/logo/index.html
    """

    @type_checker
    def add(
            self,
            *,
            code: Text,
            file_content: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add logo.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/logo/crm-timeline-logo-add.html

        This method adds a new logo.

        Args:
            code: Logo code;

            file_content: Base64 encoded content of the icon file, where file requirements are:

                - type: png,

                - size: 60x60 pixels,

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
        """Get information about the logo.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/logo/crm-timeline-logo-get.html

        This method retrieves information about the logo of the timeline log entry.

        Args:
            code: Logo code;

            timeout: Timeout in seconds.

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
        """Get a list of available logos.

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/logo/crm-timeline-logo-list.html

        This method retrieves a list of available logos for timeline log entries.

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
        """Delete logo

        Documentation: https://apidocs.bitrix24.com/api-reference/crm/timeline/logmessage/logo/crm-timeline-logo-delete.html

        This method deletes the logo.

        Args:
            code: Logo code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """
        return super().delete(code=code, timeout=timeout)
