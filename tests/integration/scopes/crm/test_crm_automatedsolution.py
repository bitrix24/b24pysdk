from typing import Generator, List, Text, Tuple

import pytest
from _pytest.cacheprovider import Cache

from b24pysdk.api.responses import BitrixAPIListFastResponse, BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.crm,
    pytest.mark.crm_automatedsolution,
]

_FIELDS: Tuple[Text, ...] = ("id", "title", "typeIds")
_TITLE: Text = f"{SDK_NAME} Digital Workplace"
_TYPE_IDS: List[int] = []
_UPDATED_TITLE: Text = f"{SDK_NAME} Updated Digital Workplace"


@pytest.mark.dependency(name="test_crm_automatedsolution_fields")
def test_crm_automatedsolution_fields(bitrix_client: BaseClient):
    """Test retrieving digital workplace fields."""

    bitrix_response = bitrix_client.crm.automatedsolution.fields().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    fields = bitrix_response.result

    for field in _FIELDS:
        assert field in fields, f"Field '{field}' should be present"
        assert isinstance(fields[field], dict), f"Field '{field}' should be a dictionary"


@pytest.mark.dependency(name="test_crm_automatedsolution_add")
def test_crm_automatedsolution_add(bitrix_client: BaseClient, cache: Cache):
    """Test creating a new digital workplace."""

    bitrix_response = bitrix_client.crm.automatedsolution.add(
        fields={
            "title": _TITLE,
            "typeIds": _TYPE_IDS,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "automatedSolution" in result, "Result should contain 'automatedSolution' key"

    automated_solution = result["automatedSolution"]

    assert isinstance(automated_solution, dict)
    assert "id" in automated_solution, "Automated solution should have 'id' field"
    assert isinstance(automated_solution["id"], int)

    automated_solution_id = automated_solution["id"]

    assert automated_solution_id > 0, "Digital workplace creation should return a positive ID"
    assert automated_solution.get("title") == _TITLE, "Digital workplace title does not match"
    assert automated_solution.get("typeIds") == _TYPE_IDS, "Digital workplace typeIds does not match"

    cache.set("automated_solution_id", automated_solution_id)


@pytest.mark.dependency(name="test_crm_automatedsolution_get", depends=["test_crm_automatedsolution_add"])
def test_crm_automatedsolution_get(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a digital workplace by ID."""

    automated_solution_id = cache.get("automated_solution_id", None)
    assert isinstance(automated_solution_id, int), "Automated solution ID should be cached after addition"

    bitrix_response = bitrix_client.crm.automatedsolution.get(
        bitrix_id=automated_solution_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "automatedSolution" in result, "Result should contain 'automatedSolution' key"

    automated_solution = result["automatedSolution"]

    assert isinstance(automated_solution, dict)
    assert automated_solution.get("id") == automated_solution_id, f"Digital workplace ID does not match. Expected: {automated_solution_id}, Got: {automated_solution.get('id')}"
    assert automated_solution.get("title") == _TITLE, "Digital workplace title does not match"
    assert automated_solution.get("typeIds") == _TYPE_IDS, "Digital workplace typeIds does not match"


@pytest.mark.dependency(name="test_crm_automatedsolution_update", depends=["test_crm_automatedsolution_get"])
def test_crm_automatedsolution_update(bitrix_client: BaseClient, cache: Cache):
    """Test updating an existing digital workplace."""

    automated_solution_id = cache.get("automated_solution_id", None)
    assert isinstance(automated_solution_id, int), "Automated solution ID should be cached"

    bitrix_response = bitrix_client.crm.automatedsolution.update(
        bitrix_id=automated_solution_id,
        fields={
            "title": _UPDATED_TITLE,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "automatedSolution" in result, "Result should contain 'automatedSolution' key"

    automated_solution = result["automatedSolution"]

    assert isinstance(automated_solution, dict)
    assert automated_solution.get("id") == automated_solution_id, f"Digital workplace ID does not match. Expected: {automated_solution_id}, Got: {automated_solution.get('id')}"
    assert automated_solution.get("title") == _UPDATED_TITLE, "Digital workplace updated title does not match"
    assert automated_solution.get("typeIds") == _TYPE_IDS, "Digital workplace typeIds does not match"


@pytest.mark.dependency(name="test_crm_automatedsolution_list", depends=["test_crm_automatedsolution_update"])
def test_crm_automatedsolution_list(bitrix_client: BaseClient, cache: Cache):
    """Test retrieving a list of digital workplaces."""

    automated_solution_id = cache.get("automated_solution_id", None)
    assert isinstance(automated_solution_id, int), "Automated solution ID should be cached"

    bitrix_response = bitrix_client.crm.automatedsolution.list(
        filter={
            "id": automated_solution_id,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict)

    result = bitrix_response.result

    assert "automatedSolutions" in result, "Result should contain 'automatedSolutions' key"

    automated_solutions = result["automatedSolutions"]

    assert isinstance(automated_solutions, list)
    assert len(automated_solutions) == 1, "Expected one digital workplace to be returned"

    automated_solution = automated_solutions[0]

    assert isinstance(automated_solution, dict)

    assert automated_solution.get("id") == automated_solution_id, f"Digital workplace ID does not match. Expected: {automated_solution_id}, Got: {automated_solution.get('id')}"
    assert automated_solution.get("title") == _UPDATED_TITLE, "Digital workplace updated title does not match"
    assert automated_solution.get("typeIds") == _TYPE_IDS, "Digital workplace typeIds does not match"


@pytest.mark.dependency(name="test_crm_automatedsolution_list_as_list", depends=["test_crm_automatedsolution_update"])
def test_crm_automatedsolution_list_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.automatedsolution.list().as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list)

    automated_solutions = bitrix_response.result

    assert len(automated_solutions) >= 1, "Expected at least one address to be returned"

    for automated_solution in automated_solutions:
        assert isinstance(automated_solution, dict)


@pytest.mark.dependency(name="test_crm_automatedsolution_list_as_list_fast", depends=["test_crm_automatedsolution_update"])
def test_crm_automatedsolution_list_as_list_fast(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.crm.automatedsolution.list().as_list_fast(descending=True).response

    assert isinstance(bitrix_response, BitrixAPIListFastResponse)
    assert isinstance(bitrix_response.result, Generator)

    automated_solutions = bitrix_response.result

    last_automated_solutions_id = None

    for automated_solution in automated_solutions:
        assert isinstance(automated_solution, dict)
        assert "id" in automated_solution

        automated_solution_id = automated_solution["id"]

        if last_automated_solutions_id is None:
            last_automated_solutions_id = automated_solution_id
        else:
            assert last_automated_solutions_id > automated_solution_id
            last_automated_solutions_id = automated_solution_id


@pytest.mark.dependency(name="test_crm_automatedsolution_delete", depends=["test_crm_automatedsolution_list_as_list_fast"])
def test_crm_automatedsolution_delete(bitrix_client: BaseClient, cache: Cache):
    """Test deleting a digital workplace."""

    automated_solution_id = cache.get("automated_solution_id", None)
    assert isinstance(automated_solution_id, int), "Automated solution ID should be cached"

    bitrix_response = bitrix_client.crm.automatedsolution.delete(
        bitrix_id=automated_solution_id,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_deleted = bitrix_response.result

    assert is_deleted is None, "Digital workplace deletion should return None"
