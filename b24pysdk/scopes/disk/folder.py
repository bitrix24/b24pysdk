from typing import Dict, Iterable, Optional, Sequence, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24Bool, B24File, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Folder",
]


class Folder(BaseEntity):
    """Handle folder actions related to Bitrix24 Disk.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/
    """

    @type_checker
    def addsubfolder(
            self,
            bitrix_id: int,
            data: Dict,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a subfolder in the specified folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-add-subfolder.html

        The method creates a subfolder.

        Args:
            bitrix_id: The ID of the folder;
            data: Dictionary describing the folder, requires NAME field;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addsubfolder,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def copyto(
            self,
            bitrix_id: int,
            target_folder_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Copy a folder to the specified target folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-copy-to.html

        The method copies a folder to the specified folder.

        Args:
            bitrix_id: The ID of the folder to copy;
            target_folder_id: The ID of the target folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest with the copied folder structure.
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
    def deletetree(
            self,
            bitrix_id: int,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Permanently delete a folder and all its sub-elements.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-delete-tree.html

        The method permanently deletes a folder and all its subitems.

        Args:
            bitrix_id: The ID of the folder to delete;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest indicating the success of deletion.
        """

        params = {
            "id": bitrix_id,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.deletetree,
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
        Retrieve a folder by its ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-get.html

        The method returns a folder by its ID.

        Args:
            bitrix_id: The ID of the folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest with the folder details.
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
        Get a public link to the folder by its ID.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-get-external-link.html

        The method returns a public link by folder ID.

        Args:
            bitrix_id: The ID of the folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest with the public link information.
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
    def getchildren(
            self,
            bitrix_id: int,
            *,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        List files and folders directly under a specified folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-get-children.html

        The method returns a list of files and folders that are directly in the folder.

        Args:
            bitrix_id: The ID of the folder;
            filter: Filter based on fields described in disk.folder.getfields;
            start: Starting item number for retrieval;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest with list of files and folders.
        """

        params = {
            "id": bitrix_id,
        }

        if filter is not None:
            params["filter"] = filter

        if start is not None:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.getchildren,
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
        Get description of folder fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-get-fields.html

        The method returns the description of folder fields.

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest with field descriptions.
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
        Move a folder to the trash bin.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-mark-deleted.html

        The method moves a folder to the trash.

        Args:
            bitrix_id: The ID of the folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest indicating success of to trash action.
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
        Move a folder to another folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-move-to.html

        The method moves a folder to the specified folder.

        Args:
            bitrix_id: The ID of the folder to move;
            target_folder_id: The ID of the destination folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest with the moved folder structure.
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
        Rename a folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-rename.html

        The method renames a folder.

        Args:
            bitrix_id: The ID of the folder to rename;
            new_name: The new name for the folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest indicating the success of renaming.
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
        Restore a folder from the trash bin.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-restore.html

        The method restores a folder from the trash.

        Args:
            bitrix_id: The ID of the folder to restore;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest indicating the success of restore action.
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
    def uploadfile(
            self,
            bitrix_id: int,
            file_content: Sequence[Text],
            data: JSONDict,
            *,
            generate_unique_name: Optional[bool] = None,
            rights: Optional[Iterable[Dict]] = None,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Upload a new file into the specified folder.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/folder/disk-folder-upload-file.html

        The method uploads a new file to the specified folder.

        Args:
            bitrix_id: The ID of the folder;
            file_content: File content encoded in base64;
            data: Dictionary describing the file, requires NAME field;
            generate_unique_name: Whether to generate a unique name in case of conflicts;
            rights: Access rights for the file;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest indicating success of the upload.
        """

        params = {
            "id": bitrix_id,
            "fileContent": B24File(file_content).to_b24(),
            "data": data,
        }

        if generate_unique_name is not None:
            params["generateUniqueName"] = B24Bool(generate_unique_name).to_b24()

        if rights is not None:
            if rights.__class__ is not list:
                rights = list(rights)

            params["rights"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.uploadfile,
            params=params,
            timeout=timeout,
        )
