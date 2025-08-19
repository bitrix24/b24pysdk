from abc import abstractmethod
from typing import TYPE_CHECKING, Text

from .....bitrix_api.classes import BitrixAPIRequest
from .....utils.types import Timeout
from ...base_crm import BaseCRM

if TYPE_CHECKING:
    from ..timeline import Timeline


class Image(BaseCRM):
    """The class is a base class for logo and icon classes.
    """

    def __init__(self, timeline: "Timeline"):
        super().__init__(timeline._scope)
        self._path = self._get_path(timeline)

    @abstractmethod
    def add(
            self,
            *,
            code: Text,
            file_content: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Add new visual element.

        This method adds a new image (logo or icon).

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

        return self._make_bitrix_api_request(
            api_method=self.add,
            params=params,
            timeout=timeout,
        )

    @abstractmethod
    def get(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get information about the image.

        This method retrieves information about an image (logo or icon) of the timeline log entry.

        Args:
            code: Image element code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_method=self.get,
            params=params,
            timeout=timeout,
        )

    @abstractmethod
    def list(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Get a list of available image.

        This method retrieves a list of available images (icons or logos) for timeline log entries.

        """
        return self._list(timeout=timeout)

    @abstractmethod
    def delete(
            self,
            *,
            code: Text,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """Delete image.

        This method deletes an image.

        Args:
            code: Image code;

            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest
        """

        params = {
            "code": code,
        }

        return self._make_bitrix_api_request(
            api_method=self.delete,
            params=params,
            timeout=timeout,
        )
