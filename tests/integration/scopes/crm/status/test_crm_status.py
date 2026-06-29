from typing import Generator, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse, BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.field import CRMField, CRMFieldsDict

from .....constants import SDK_NAME, SORT

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_status,
]

_FIELDS: Tuple[Text, ...] = (
    "ID",
    "ENTITY_ID",
    "STATUS_ID",
    "SORT",
    "NAME",
    "NAME_INIT",
    "SYSTEM",
    "CATEGORY_ID",
    "COLOR",
    "SEMANTICS",
    "EXTRA",
)
_ENTITY_ID: Text = "SOURCE"
_STATUS_ID: Text = f"{SDK_NAME.upper()}_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
_NAME: Text = f"{SDK_NAME} Status"
_UPDATED_NAME: Text = f"{SDK_NAME} Updated Status"
_SORT: int = SORT
_UPDATED_SORT: int = SORT + 1


def _assert_status(status: dict, *, name: Text, sort: int) -> None:
    """Assert common CRM status dictionary item fields."""

    assert isinstance(status, dict)
    assert status.get("ENTITY_ID") == _ENTITY_ID, "Status ENTITY_ID does not match"
    assert status.get("STATUS_ID") == _STATUS_ID, "Status STATUS_ID does not match"
    assert status.get("NAME") == name, "Status NAME does not match"
    assert int(status.get("SORT", 0)) == sort, "Status SORT does not match"
    assert status.get("SYSTEM") == "N", "Test status should not be system"


def test_crm_status_fields(bitrix_client: BaseClient):
    """Test retrieving CRM status field descriptions."""

    bitrix_response = bitrix_client.crm.status.fields().response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    fields = bitrix_response.value

    assert isinstance(fields, CRMFieldsDict)

    for field in _FIELDS:
        assert field in fields, f"Field {field!r} should be present"
        assert isinstance(fields[field], CRMField), f"Field {field!r} should be CRMField"


@pytest.mark.dependency(name="test_crm_status_add")
def test_crm_status_add(bitrix_client: BaseClient, cache: Cache):
    """Test creating a CRM status dictionary item."""

    bitrix_response = bitrix_client.crm.status.add(
        fields={
            "ENTITY_ID": _ENTITY_ID,
            "STATUS_ID": _STATUS_ID,
            "NAME": _NAME,
            "SORT": _SORT,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int)

    status_id = bitrix_response.result

    assert status_id > 0, "Status creation should return a positive ID"

    cache.set("crm_status_id", status_id)


@pytest.mark.dependency(name="test_crm_status_get", depends=["test_crm_status_add"])
def test_crm_status_get(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a CRM status dictionary item by ID."""

    status_id = cache.get("crm_status_id", None)
    assert isinstance(status_id, int), "Status ID should be cached after creation"

    bitrix_response = bitrix_client.crm.status.get(bitrix_id=status_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    status = bitrix_response.result

    assert int(status.get("ID", 0)) == status_id, "Status ID does not match"
    _assert_status(status, name=_NAME, sort=_SORT)


@pytest.mark.dependency(name="test_crm_status_update", depends=["test_crm_status_get"])
def test_crm_status_update(bitrix_client: BaseClient, cache: Cache):
    """Test updating an existing CRM status dictionary item."""

    status_id = cache.get("crm_status_id", None)
    assert isinstance(status_id, int), "Status ID should be cached"

    bitrix_response = bitrix_client.crm.status.update(
        bitrix_id=status_id,
        fields={
            "NAME": _UPDATED_NAME,
            "SORT": _UPDATED_SORT,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_updated = bitrix_response.result

    assert is_updated is True, "Status update should return True"


@pytest.mark.dependency(name="test_crm_status_list", depends=["test_crm_status_update"])
def test_crm_status_list(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving CRM status dictionary items by filter."""

    status_id = cache.get("crm_status_id", None)
    assert isinstance(status_id, int), "Status ID should be cached"

    bitrix_response = bitrix_client.crm.status.list(
        filter={
            "ENTITY_ID": _ENTITY_ID,
            "STATUS_ID": _STATUS_ID,
        },
        order={"SORT": "ASC"},
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list)

    statuses = bitrix_response.result

    assert len(statuses) == 1, "Expected one CRM status to be returned"

    status = statuses[0]

    assert isinstance(status, dict)
    assert int(status.get("ID", 0)) == status_id, "Status ID does not match"
    _assert_status(status, name=_UPDATED_NAME, sort=_UPDATED_SORT)


@pytest.mark.dependency(name="test_crm_status_list_as_list", depends=["test_crm_status_update"])
def test_crm_status_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.status.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    statuses = bitrix_response.result

    assert len(statuses) >= 1, "Expected at least one CRM status to be returned"

    for status in statuses:
        assert isinstance(status, dict)


@pytest.mark.dependency(name="test_crm_status_list_as_list_fast", depends=["test_crm_status_update"])
def test_crm_status_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.status.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    statuses = bitrix_response.result

    last_status_id = None

    for status in statuses:
        assert isinstance(status, dict)
        assert "ID" in status

        status_id = int(status["ID"])

        if last_status_id is None:
            last_status_id = status_id
        else:
            assert last_status_id > status_id
            last_status_id = status_id


@pytest.mark.dependency(name="test_crm_status_delete", depends=["test_crm_status_add"])
def test_crm_status_delete(bitrix_client: BaseClient, cache: Cache):
    """Test deleting a CRM status dictionary item."""

    status_id = cache.get("crm_status_id", None)
    assert isinstance(status_id, int), "Status ID should be cached"

    bitrix_response = bitrix_client.crm.status.delete(bitrix_id=status_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result

    assert is_deleted is True, "Status deletion should return True"
