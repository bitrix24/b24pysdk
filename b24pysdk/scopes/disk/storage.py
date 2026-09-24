from typing import Iterable, Optional, Sequence, Text

from ..._constants import MISSING
from ...api.requests import BitrixAPIRequest
from ...utils.converters import bool_to_bitrix
from ...utils.functional import type_checker
from ...utils.types import B24File, JSONDict, JSONList, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Storage",
]


class Storage(BaseEntity):
    """Handle operations related to Bitrix24 storage.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/
    """

    @type_checker
    def add_folder(
            self,
            bitrix_id: int,
            data: JSONDict,
            *,
            rights: Optional[JSONList] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Create a new folder in the storage root.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-add-folder.html

        Args:
            bitrix_id: Identifier for the storage;
            data: Object format:
                {
                    'NAME': 'New folder name'
                };
            rights: Access rights for the folder;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "data": data,
        }

        if rights is not MISSING:
            if rights.__class__ is not list:
                rights = list(rights)

            params["rights"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.add_folder,
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
        Retrieve storage by its identifier.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get.html

        Args:
            bitrix_id: Identifier for the storage;
            timeout: Timeout in seconds.

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
    def get_children(
            self,
            bitrix_id: int,
            *,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve list of files and folders in the storage root.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get-children.html

        Args:
            bitrix_id: Identifier for the storage;
            filter: Object format:
                {
                    'field': 'value'
                };
            order: Sort order based on fields described in disk.storage.getfields;
            start: Starting point for element retrieval;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get_children,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_fields(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve description of storage fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get-fields.html

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_fields,
            timeout=timeout,
        )

    @type_checker
    def get_for_app(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve storage information applicable for the app.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get-for-app.html

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_for_app,
            timeout=timeout,
        )

    @type_checker
    def get_list(
            self,
            *,
            filter: Optional[JSONDict] = MISSING,
            order: Optional[JSONDict] = MISSING,
            start: Optional[int] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve list of available storage.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get-list.html

        Args:
            filter: Object format:
                {
                    'field': 'value'
                };
            order: Sort order based on fields described in disk.storage.getfields;
            start: Starting point for element retrieval;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params: JSONDict = {}

        if filter is not MISSING:
            params["filter"] = filter

        if order is not MISSING:
            params["order"] = order

        if start is not MISSING:
            params["start"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.get_list,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def get_types(
            self,
            *,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Retrieve list of storage types.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get-types.html

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.get_types,
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
        Rename the storage.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-rename.html

        Args:
            bitrix_id: Identifier for the storage;
            new_name: New name for the storage;
            timeout: Timeout in seconds.

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
    def upload_file(
            self,
            bitrix_id: int,
            file_content: Sequence[Text],
            data: JSONDict,
            *,
            generate_unique_name: Optional[bool] = MISSING,
            rights: Optional[Iterable[JSONDict]] = MISSING,
            timeout: Timeout = None,
    ) -> BitrixAPIRequest:
        """
        Upload a new file to the storage root.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-upload-file.html

        Args:
            bitrix_id: Identifier for the storage;
            file_content: File content in bytes for the upload;
            data: Object format:
                {
                    'NAME': 'File name'
                };
            generate_unique_name: Whether to create a unique name for the file;
            rights: List of rights to be assigned to the file;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "fileContent": B24File(file_content).to_b24(),
            "data": data,
        }

        if generate_unique_name is not MISSING:
            params["generateUniqueName"] = bool_to_bitrix(generate_unique_name)

        if rights is not MISSING:
            if rights.__class__ is not list:
                rights = list(rights)

            params["rights"] = rights

        return self._make_bitrix_api_request(
            api_wrapper=self.upload_file,
            params=params,
            timeout=timeout,
        )

