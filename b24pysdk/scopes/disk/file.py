from typing import Optional, Sequence, Text

from ...api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24File, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "File",
]


class File(BaseEntity):
    """Handle operations related to Bitrix24 disk files.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/
    """

    @type_checker
    def copyto(
            self,
            bitrix_id: int,
            target_folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Copy a file to a target folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-copy-to.html

        Args:
            bitrix_id: The ID of the file to be copied;

            target_folder_id: The ID of the folder where the file should be copied.

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "targetFolderId": target_folder_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.copyto,
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
        """
        Delete a file by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-delete.html

        Args:
            bitrix_id: The ID of the file to be deleted;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
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
        """
        Retrieve file details by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-get.html

        Args:
            bitrix_id: The ID of the file to retrieve information about;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_external_link(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Get an external link for a file.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-get-external-link.html

        Args:
            bitrix_id: The ID of the file for which to get an external link;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.get_external_link,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_versions(
            self,
            bitrix_id: int,
            *,
            filter: Optional[JSONDict] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve the versions of a file.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-get-versions.html

        Args:
            bitrix_id: The ID of the file whose versions are to be retrieved;

            filter: Object format to filter versions;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        if filter is not None:
            params["filter"] = filter

        return self._make_bitrix_api_request(
            api_wrapper=self.get_versions,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def getfields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve fields available for files.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-get-fields.html

        Args:
            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

    @type_checker
    def markdeleted(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Mark a file as deleted by ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-mark-deleted.html

        Args:
            bitrix_id: The ID of the file to be marked as deleted;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.markdeleted,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def moveto(
            self,
            bitrix_id: int,
            target_folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Move a file to a target folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-move-to.html

        Args:
            bitrix_id: The ID of the file to be moved;

            target_folder_id: The ID of the folder to move the file to;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "targetFolderId": target_folder_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.moveto,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def rename(
            self,
            bitrix_id: int,
            new_name: Text,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Rename a file.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-rename.html

        Args:
            bitrix_id: The ID of the file to rename;

            new_name: The new name for the file;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "newName": new_name,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.rename,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def restore(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Restore a file from the recycle bin.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-restore.html

        Args:
            bitrix_id: The ID of the file to restore;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.restore,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def restore_from_version(
            self,
            bitrix_id: int,
            version_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Restore a file to a specific version.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-restore-from-version.html

        Args:
            bitrix_id: The ID of the file to restore;

            version_id: The ID of the version to restore the file to;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "versionId": version_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.restore_from_version,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def uploadversion(
            self,
            bitrix_id: int,
            file_content: Sequence[Text],
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Upload a new version of a file.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/file/disk-file-upload-version.html

        Args:
            bitrix_id: The ID of the file to upload a new version for;

            file_content: The content of the file to be uploaded;

            timeout: Timeout for the request in seconds.

        Returns:
            Instance of BitrixAPIRequest.

        """

        params = {
            "id": bitrix_id,
            "fileContent": B24File(file_content).to_b24(),
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.uploadversion,
            params=params,
            timeout=timeout,
        )

