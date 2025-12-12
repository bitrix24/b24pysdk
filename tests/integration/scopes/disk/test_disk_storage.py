from typing import List, Text, Tuple, cast

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Client, Config
from b24pysdk.bitrix_api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.utils.types import JSONDictGenerator
from tests.constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.disk,
    pytest.mark.storage,
]

_STORAGE_ID: int = 215
_NAME: Text = f"{SDK_NAME} New Folder"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Storage"
_FILE_NAME: Text = f"{SDK_NAME}_test_file.txt"
_FILE_CONTENT: List[Text] = [f"{SDK_NAME}_test_file.txt", "SGVsbG8gV29ybGQ="]

_EXPECTED_TYPES: Tuple = ("user", "common", "group")

_FIELDS: Tuple[Text, ...] = (
    "ID",
    "NAME",
    "CODE",
    "MODULE_ID",
    "ENTITY_TYPE",
    "ENTITY_ID",
    "ROOT_OBJECT_ID",
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
    "ENTITY_TYPE": "user",
}
_START: int = 0


@pytest.mark.dependency(name="test_disk_storage_getfields")
def test_disk_storage_getfields(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getfields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_disk_storage_get", depends=["test_disk_storage_getfields"])
def test_disk_storage_get(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.get(
        bitrix_id=_STORAGE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    storage = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in storage, f"Field '{field}' should be present"

    assert storage.get("ID") == str(_STORAGE_ID), "Storage ID does not match"


@pytest.mark.dependency(name="test_disk_storage_gettypes", depends=["test_disk_storage_get"])
def test_disk_storage_gettypes(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.gettypes().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    types = cast(list, bitrix_response.result)

    assert len(types) >= 1, "Expected at least one storage type"

    for storage_type in types:
        assert isinstance(storage_type, Text)
        assert storage_type in _EXPECTED_TYPES, f"Storage type '{storage_type}' should be one of {_EXPECTED_TYPES}"


@pytest.mark.dependency(name="test_disk_storage_gettypes_as_list", depends=["test_disk_storage_gettypes"])
def test_disk_storage_gettypes_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.gettypes().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    types = cast(list, bitrix_response.result)

    assert len(types) >= 1, "Expected at least one storage type"

    for storage_type in types:
        assert isinstance(storage_type, Text)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_disk_storage_getforapp", depends=["test_disk_storage_gettypes_as_list"])
def test_disk_storage_getforapp(bitrix_client: Client, cache: Cache):
    """"""

    bitrix_response = bitrix_client.disk.storage.getforapp().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    storage = cast(dict, bitrix_response.result)

    for field in _FIELDS:
        assert field in storage, f"Field '{field}' should be present"

    cache.set("app_storage_id", int(storage["ID"]))


@pytest.mark.dependency(name="test_disk_storage_getlist", depends=["test_disk_storage_getforapp"])
def test_disk_storage_getlist(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getlist(
        filter=_FILTER,
        start=_START,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    storages = cast(list, bitrix_response.result)

    assert len(storages) >= 1, "Expected at least one storage"

    storage = storages[0]

    assert isinstance(storage, dict)

    for field in _FIELDS:
        assert field in storage, f"Field '{field}' should be present"


@pytest.mark.dependency(name="test_disk_storage_getlist_as_list", depends=["test_disk_storage_getlist"])
def test_disk_storage_getlist_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getlist().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    storages = cast(list, bitrix_response.result)

    for storage in storages:
        assert isinstance(storage, dict)


@pytest.mark.dependency(name="test_disk_storage_getlist_as_list_fast", depends=["test_disk_storage_getlist_as_list"])
def test_disk_storage_getlist_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getlist().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)

    storages = cast(JSONDictGenerator, bitrix_response.result)

    last_storage_id = None

    for storage in storages:
        assert isinstance(storage, dict)
        assert "ID" in storage

        storage_id = int(storage["ID"])

        if last_storage_id is None:
            last_storage_id = storage_id
        else:
            assert last_storage_id > storage_id
            last_storage_id = storage_id


@pytest.mark.dependency(name="test_disk_storage_getchildren", depends=["test_disk_storage_getlist_as_list_fast"])
def test_disk_storage_getchildren(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getchildren(
        bitrix_id=_STORAGE_ID,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    children = cast(list, bitrix_response.result)

    assert len(children) >= 1, "Expected at least one user field to be returned"

    children = children[0]

    assert isinstance(children, dict)


@pytest.mark.dependency(name="test_disk_storage_getchildren_as_list", depends=["test_disk_storage_getchildren"])
def test_disk_storage_getchildren_as_list(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getchildren(bitrix_id=_STORAGE_ID).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    children = cast(list, bitrix_response.result)

    for child in children:
        assert isinstance(child, dict)


@pytest.mark.dependency(name="test_disk_storage_getchildren_as_list_fast", depends=["test_disk_storage_getchildren_as_list"])
def test_disk_storage_getchildren_as_list_fast(bitrix_client: Client):
    """"""

    bitrix_response = bitrix_client.disk.storage.getchildren(bitrix_id=_STORAGE_ID).as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)

    children = cast(JSONDictGenerator, bitrix_response.result)

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


@pytest.mark.dependency(name="test_disk_storage_addfolder", depends=["test_disk_storage_getchildren_as_list"])
def test_disk_storage_addfolder(bitrix_client: Client):
    """"""

    unique_name = f"{_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.storage.addfolder(
        bitrix_id=_STORAGE_ID,
        data={"NAME": unique_name},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    folder = cast(dict, bitrix_response.result)

    for field in _CHILDREN_FIELDS:
        assert field in folder, f"Field '{field}' should be present"

    assert folder.get("NAME") == unique_name, "Folder NAME does not match"
    assert folder.get("STORAGE_ID") == str(_STORAGE_ID), "Folder STORAGE_ID does not match"
    assert folder.get("TYPE") == "folder", "Folder TYPE should be 'folder'"


@pytest.mark.dependency(name="test_disk_storage_uploadfile", depends=["test_disk_storage_addfolder"])
def test_disk_storage_uploadfile(bitrix_client: Client):
    """"""

    unique_file_name = f"{_FILE_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.storage.uploadfile(
        bitrix_id=_STORAGE_ID,
        file_content=_FILE_CONTENT,
        data={"NAME": unique_file_name},
        generate_unique_name=True,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    file = cast(dict, bitrix_response.result)

    for field in _CHILDREN_FIELDS:
        assert field in file, f"Field '{field}' should be present"

    assert unique_file_name in file.get("NAME", ""), f"File NAME should contain '{unique_file_name}'"
    assert file.get("STORAGE_ID") == str(_STORAGE_ID), "File STORAGE_ID does not match"
    assert file.get("TYPE") == "file", "File TYPE should be 'file'"


@pytest.mark.dependency(name="test_disk_storage_rename", depends=["test_disk_storage_get"])
def test_disk_storage_rename(bitrix_client: Client, cache: Cache):
    """"""

    app_storage_id = cache.get("app_storage_id", None)
    assert isinstance(app_storage_id, int), "App storage ID should be cached"

    unique_name = f"{_UPDATED_NAME}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.disk.storage.rename(
        bitrix_id=app_storage_id,
        new_name=unique_name,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    updated_storage = cast(dict, bitrix_response.result)

    assert updated_storage.get("ID") == str(app_storage_id), "Storage ID should remain the same"
    assert updated_storage.get("NAME") == unique_name, "Storage NAME should be updated"
