import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient
from b24pysdk.errors import BitrixAPIError

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.im,
]

_FOLDER_FIELDS = ("ID",)


def test_disk_folder_get(bitrix_client: BaseClient):
    """"""

    chat_id_response = bitrix_client.im.chat.add(users=[BITRIX_PORTAL_OWNER_ID], type="CHAT").response
    assert isinstance(chat_id_response, BitrixAPIResponse)
    assert isinstance(chat_id_response.result, int), "im.chat.add should return chat id"

    bitrix_response = bitrix_client.im.disk.folder.get(chat_id=chat_id_response.result).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "im.disk.folder.get result should be a dict"

    folder_data = bitrix_response.result

    for field in _FOLDER_FIELDS:
        assert field in folder_data, f"Field '{field}' should be present"


def test_disk_file_save(bitrix_client: BaseClient):
    """"""

    with pytest.raises(BitrixAPIError):
        _ = bitrix_client.im.disk.file.save(disk_id=0).response


def test_disk_file_delete(bitrix_client: BaseClient):
    """"""

    with pytest.raises(BitrixAPIError):
        _ = bitrix_client.im.disk.file.delete(chat_id=0, disk_id=0).response


def test_disk_file_commit(bitrix_client: BaseClient):
    """"""

    with pytest.raises(BitrixAPIError):
        _ = bitrix_client.im.disk.file.commit(chat_id=0, upload_id=0, disk_id=0).response
