from typing import List, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient
from tests.constants import SDK_NAME

pytestmark = [
    # pytest.mark.integration,
    pytest.mark.disk,
    pytest.mark.folder,
]

_FOLDER_ID: int = 293
_FOLDER_TYPE: Text = "folder"
_NAME: Text = f"{SDK_NAME} Test Folder"
_SUBFOLDER_NAME: Text = f"{SDK_NAME} Test Subfolder"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Folder"
_FILE_NAME: Text = f"{SDK_NAME}_folder_test_file.txt"
_FILE_CONTENT: List[Text] = [f"{SDK_NAME}_folder_test_file.txt", "SGVsbG8gV29ybGQ="]

_FIELDS: Tuple[Text, ...] = (
    "ID",
    "NAME",
    "CODE",
    "STORAGE_ID",
    "TYPE",
    "PARENT_ID",
    "DELETED_TYPE",
    "CREATE_TIME",
    "UPDATE_TIME",
    "DELETE_TIME",
    "CREATED_BY",
    "UPDATED_BY",
    "DELETED_BY",
)

_FOLDER_FIELDS_INFO: Tuple[Text, ...] = (
    "ID",
    "NAME",
    "TYPE",
    "CODE",
    "STORAGE_ID",
    "REAL_OBJECT_ID",
    "PARENT_ID",
    "CREATE_TIME",
    "UPDATE_TIME",
    "DELETE_TIME",
    "CREATED_BY",
    "UPDATED_BY",
    "DELETED_BY",
    "DELETED_TYPE",
)

_CHILDREN_FIELDS: Tuple[Text, ...] = (
    "ID",
    "NAME",
    "CODE",
    "STORAGE_ID",
    "TYPE",
    "PARENT_ID",
    "DELETED_TYPE",
    "CREATE_TIME",
    "UPDATE_TIME",
    "DELETE_TIME",
    "CREATED_BY",
    "UPDATED_BY",
    "DELETED_BY",
)

_FILTER = {
    "TYPE": "folder",
}
_START: int = 0


@pytest.mark.dependency(name="test_disk_folder_getfields")
def test_disk_folder_getfields(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.disk.folder.getfields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FOLDER_FIELDS_INFO:
        assert field in fields, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_disk_folder_get", depends=["test_disk_folder_getfields"])
def test_disk_folder_get(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.disk.folder.get(
        bitrix_id=_FOLDER_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    folder = bitrix_response.result

    for field in _FIELDS:
        assert field in folder, f"Field '{field}' should be present"

    assert folder.get("ID") == str(_FOLDER_ID), "Folder ID does not match"
    assert folder.get("TYPE") == _FOLDER_TYPE, "Folder TYPE should be 'folder'"


@pytest.mark.dependency(name="test_disk_folder_getchildren", depends=["test_disk_folder_get"])
def test_disk_folder_getchildren(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.disk.folder.getchildren(
        bitrix_id=_FOLDER_ID,
        filter=_FILTER,
        start=_START,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    children = bitrix_response.result

    assert len(children) >= 1, "Expected at least one user field to be returned"

    child = children[0]

    assert isinstance(child, dict)

    for field in _CHILDREN_FIELDS:
        assert field in child, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_disk_folder_getchildren_as_list", depends=["test_disk_folder_getchildren"])
def test_disk_folder_getchildren_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.disk.folder.getchildren(bitrix_id=_FOLDER_ID).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    children = bitrix_response.result

    for child in children:
        assert isinstance(child, dict)


@pytest.mark.dependency(name="test_disk_folder_getchildren_as_list_fast", depends=["test_disk_folder_getchildren_as_list"])
def test_disk_folder_getchildren_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.disk.folder.getchildren(bitrix_id=_FOLDER_ID).as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)

    children = bitrix_response.result

    last_child_id = None

    for child in children:
        assert isinstance(child, dict)
        assert "ID" in child

        child_id = int(child["ID"])

        if last_child_id is None:
            last_child_id = child_id
        else:
            assert last_child_id > child_id
            last_child_id = child_id


@pytest.mark.dependency(name="test_disk_folder_addsubfolder", depends=["test_disk_folder_getchildren_as_list_fast"])
def test_disk_folder_addsubfolder(bitrix_client: BaseClient, cache: Cache):
    """"""

    unique_name = f"{_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.folder.addsubfolder(
        bitrix_id=_FOLDER_ID,
        data={"NAME": unique_name},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    folder = bitrix_response.result

    for field in _FIELDS:
        assert field in folder, f"Field '{field}' should be present"

    assert folder.get("NAME") == unique_name, "Folder NAME does not match"
    assert folder.get("PARENT_ID") == str(_FOLDER_ID), "Folder PARENT_ID does not match"
    assert folder.get("TYPE") == "folder", "Folder TYPE should be 'folder'"

    cache.set("created_folder_id", int(folder["ID"]))


@pytest.mark.dependency(name="test_disk_folder_rename", depends=["test_disk_folder_addsubfolder"])
def test_disk_folder_rename(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    unique_name = f"{_UPDATED_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.folder.rename(
        bitrix_id=folder_id,
        new_name=unique_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    updated_folder = bitrix_response.result

    assert updated_folder.get("ID") == str(folder_id), "Folder ID should remain the same"
    assert updated_folder.get("NAME") == unique_name, "Folder NAME should be updated"


@pytest.mark.dependency(name="test_disk_folder_copyto", depends=["test_disk_folder_rename"])
def test_disk_folder_copyto(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    target_folder_name = f"{SDK_NAME}_copy_target_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    target_response = bitrix_client.disk.folder.addsubfolder(
        bitrix_id=_FOLDER_ID,
        data={"NAME": target_folder_name},
    ).response

    assert isinstance(target_response, BitrixAPIResponse)
    target_folder = target_response.result
    target_folder_id = int(target_folder["ID"])

    bitrix_response = bitrix_client.disk.folder.copyto(
        bitrix_id=folder_id,
        target_folder_id=target_folder_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    copied_folder = bitrix_response.result

    assert copied_folder.get("PARENT_ID") == str(target_folder_id), "Copied folder PARENT_ID should be target folder"


@pytest.mark.dependency(name="test_disk_folder_moveto", depends=["test_disk_folder_copyto"])
def test_disk_folder_moveto(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    temp_folder_name = f"{SDK_NAME}_temp_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.folder.addsubfolder(
        bitrix_id=_FOLDER_ID,
        data={"NAME": temp_folder_name},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    temp_folder = bitrix_response.result
    temp_folder_id = int(temp_folder["ID"])

    assert folder_id != temp_folder_id, "Cannot move folder to itself"

    bitrix_response = bitrix_client.disk.folder.moveto(
        bitrix_id=folder_id,
        target_folder_id=temp_folder_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    moved_folder = bitrix_response.result

    assert moved_folder.get("ID") == str(folder_id), "Folder ID should remain the same after move"
    assert moved_folder.get("PARENT_ID") == temp_folder_id, f"Moved folder PARENT_ID should be {temp_folder_id}, got {moved_folder.get('PARENT_ID')}"


@pytest.mark.dependency(name="test_disk_folder_uploadfile", depends=["test_disk_folder_moveto"])
def test_disk_folder_uploadfile(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    unique_file_name = f"{_FILE_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.folder.uploadfile(
        bitrix_id=folder_id,
        file_content=_FILE_CONTENT,
        data={"NAME": unique_file_name},
        generate_unique_name=True,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    file = bitrix_response.result

    for field in _CHILDREN_FIELDS:
        assert field in file, f"Field '{field}' should be present"

    assert unique_file_name in file.get("NAME", ""), f"File NAME should contain '{unique_file_name}'"
    assert file.get("PARENT_ID") == str(folder_id), "File PARENT_ID does not match"
    assert file.get("TYPE") == "file", "File TYPE should be 'file'"


@pytest.mark.dependency(name="test_disk_folder_get_external_link", depends=["test_disk_folder_uploadfile"])
def test_disk_folder_get_external_link(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    bitrix_response = bitrix_client.disk.folder.get_external_link(
        bitrix_id=folder_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    assert isinstance(bitrix_response.result, str)


@pytest.mark.dependency(name="test_disk_folder_markdeleted", depends=["test_disk_folder_get_external_link"])
def test_disk_folder_markdeleted(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    bitrix_response = bitrix_client.disk.folder.markdeleted(
        bitrix_id=folder_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    deleted_folder = bitrix_response.result

    assert deleted_folder.get("DELETED_TYPE") != "0", "Folder should be marked as deleted"


@pytest.mark.dependency(name="test_disk_folder_restore", depends=["test_disk_folder_markdeleted"])
def test_disk_folder_restore(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    bitrix_response = bitrix_client.disk.folder.restore(
        bitrix_id=folder_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    restored_folder = bitrix_response.result

    assert restored_folder.get("DELETED_TYPE") == 0, "Folder should be restored from deleted state"


@pytest.mark.dependency(name="test_disk_folder_deletetree", depends=["test_disk_folder_restore"])
def test_disk_folder_deletetree(bitrix_client: BaseClient, cache: Cache):
    """"""

    folder_id = cache.get("created_folder_id", None)
    assert isinstance(folder_id, int), "Created folder ID should be cached"

    bitrix_response = bitrix_client.disk.folder.deletetree(
        bitrix_id=folder_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool)

    is_deleted = bitrix_response.result
    assert is_deleted is True, "Folder tree deletion should return True"
