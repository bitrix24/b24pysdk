from typing import Iterable, Optional, Sequence, Text

from ...bitrix_api.requests import BitrixAPIRequest
from ...utils.functional import type_checker
from ...utils.types import B24Bool, B24File, JSONDict, Timeout
from .._base_entity import BaseEntity

__all__ = [
    "Storage",
]


class Storage(BaseEntity):
    """Handle operations related to Bitrix24 storage.

    Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/
    """

    @type_checker
    def addfolder(
            self,
            bitrix_id: int,
            data: JSONDict,
            *,
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
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
            "data": data,
        }

        return self._make_bitrix_api_request(
            api_wrapper=self.addfolder,
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
    def getchildren(
            self,
            bitrix_id: int,
            *,
            filter: Optional[JSONDict] = None,
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
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = {
            "id": bitrix_id,
        }

        if filter is not None:
            params["filter"] = filter

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
        Retrieve description of storage fields.

        Documentation: https://apidocs.bitrix24.com/api-reference/disk/storage/disk-storage-get-fields.html

        Args:
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        return self._make_bitrix_api_request(
            api_wrapper=self.getfields,
            timeout=timeout,
        )

    @type_checker
    def getforapp(
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
            api_wrapper=self.getforapp,
            timeout=timeout,
        )

    @type_checker
    def getlist(
            self,
            *,
            filter: Optional[JSONDict] = None,
            start: Optional[int] = None,
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
            start: Starting point for element retrieval;
            timeout: Timeout in seconds.

        Returns:
            Instance of BitrixAPIRequest.
        """

        params = dict()

        if filter is not None:
            params["filter"] = filter

        if start is not None:
            params["START"] = start

        return self._make_bitrix_api_request(
            api_wrapper=self.getlist,
            params=params,
            timeout=timeout,
        )

    @type_checker
    def gettypes(
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
            api_wrapper=self.gettypes,
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
    def uploadfile(
            self,
            bitrix_id: int,
            file_content: Sequence[Text],
            data: JSONDict,
            *,
            generate_unique_name: Optional[bool] = None,
            rights: Optional[Iterable[JSONDict]] = None,
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

