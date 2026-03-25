from typing import Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.calendar,
    pytest.mark.calendar_resource,
]

_RESOURCE_FIELDS: Tuple[Text, ...] = ("ID", "NAME", "CREATED_BY")
_NAME_PREFIX: Text = f"{SDK_NAME} RESOURCE"
_UPDATED_NAME: Text = f"{SDK_NAME} RESOURCE UPDATED"


@pytest.mark.dependency(name="test_calendar_resource_add")
def test_add(bitrix_client: BaseClient, cache: Cache):
    """"""

    resource_name = f"{_NAME_PREFIX} {int(Config().get_local_datetime().timestamp() * (10 ** 6))}"

    bitrix_response = bitrix_client.calendar.resource.add(name=resource_name).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.resource.add result should be int"

    resource_id = bitrix_response.result
    assert resource_id > 0, "calendar.resource.add should return positive ID"

    cache.set("calendar_resource_id", resource_id)


@pytest.mark.dependency(name="test_calendar_resource_update", depends=["test_calendar_resource_add"])
def test_update(bitrix_client: BaseClient, cache: Cache):
    """"""

    resource_id = cache.get("calendar_resource_id", None)
    assert isinstance(resource_id, int), "Resource ID should be cached"

    bitrix_response = bitrix_client.calendar.resource.update(
        resource_id=resource_id,
        name=_UPDATED_NAME,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "calendar.resource.update result should be int"
    assert bitrix_response.result > 0, "calendar.resource.update should return positive ID"


@pytest.mark.dependency(name="test_calendar_resource_list", depends=["test_calendar_resource_update"])
def test_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    resource_id = cache.get("calendar_resource_id", None)
    assert isinstance(resource_id, int), "Resource ID should be cached"

    bitrix_response = bitrix_client.calendar.resource.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "calendar.resource.list result should be a list"

    resources = bitrix_response.result
    assert len(resources) >= 1, "Expected at least one resource to be returned"

    target_resource = None
    for resource in resources:
        assert isinstance(resource, dict), "Each resource should be a dict"
        for field in _RESOURCE_FIELDS:
            assert field in resource, f"Field '{field}' should be present"

        if resource.get("ID") == str(resource_id):
            target_resource = resource

    assert target_resource is not None, "Created resource should be present in calendar.resource.list"
    assert target_resource.get("NAME") == _UPDATED_NAME, "Resource NAME does not match"


@pytest.mark.dependency(name="test_calendar_resource_delete", depends=["test_calendar_resource_list"])
def test_delete(bitrix_client: BaseClient, cache: Cache):
    """"""

    resource_id = cache.get("calendar_resource_id", None)
    assert isinstance(resource_id, int), "Resource ID should be cached"

    bitrix_response = bitrix_client.calendar.resource.delete(resource_id=resource_id).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "calendar.resource.delete result should be bool"
    assert bitrix_response.result is True, "calendar.resource.delete should return True"
