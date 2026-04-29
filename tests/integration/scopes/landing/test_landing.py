import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.landing,
]
_LANDING_FIELDS = ("ID", "TITLE")
_SITE_FIELDS = ("ID", "TYPE")
_TEMPLATE_FIELDS = ("ID", "TITLE")
_ROLE_ID_FIELDS = ("ID", "id")
_ROLE_NAME_FIELDS = ("NAME", "name", "TITLE", "title")
_BLOCK_REPOSITORY_SECTION_FIELDS = ("name", "items")
_BLOCK_REPOSITORY_ITEM_FIELDS = ("name", "namespace", "section")


def test_landing_get_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.landing.get_list(
        params={
            "select": list(_LANDING_FIELDS),
            "order": {"ID": "DESC"},
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "landing.landing.get_list result should be a list"

    for landing in bitrix_response.result:
        assert isinstance(landing, dict), "landing.landing.get_list item should be dict"
        for field in _LANDING_FIELDS:
            assert field in landing, f"Field '{field}' should be present"


def test_site_get_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.site.get_list(
        params={
            "select": list(_SITE_FIELDS),
            "order": {"ID": "DESC"},
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "landing.site.get_list result should be a list"

    for site in bitrix_response.result:
        assert isinstance(site, dict), "landing.site.get_list item should be dict"
        for field in _SITE_FIELDS:
            assert field in site, f"Field '{field}' should be present"


def test_template_getlist(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.template.getlist(
        params={
            "select": list(_TEMPLATE_FIELDS),
            "order": {"ID": "DESC"},
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "landing.template.getlist result should be a list"

    for template in bitrix_response.result:
        assert isinstance(template, dict), "landing.template.getlist item should be dict"
        for field in _TEMPLATE_FIELDS:
            assert field in template, f"Field '{field}' should be present"


def test_role_is_enabled(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.role.is_enabled().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, bool), "landing.role.is_enabled result should be bool"


def test_role_get_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.role.get_list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "landing.role.get_list result should be a list"
    assert len(bitrix_response.result) > 0, "landing.role.get_list should return at least one item"

    for role in bitrix_response.result:
        assert isinstance(role, dict), "landing.role.get_list item should be dict"
        assert any(field in role for field in _ROLE_ID_FIELDS), "Role ID field should be present"
        assert any(field in role for field in _ROLE_NAME_FIELDS), "Role name field should be present"


def test_block_getrepository(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.landing.block.getrepository().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, dict), "landing.block.getrepository result should be a dict"

    sections = bitrix_response.result

    for section_name, section_data in sections.items():
        assert isinstance(section_name, str), "landing.block.getrepository section key should be str"
        assert isinstance(section_data, dict), "landing.block.getrepository section should be a dict"
        for field in _BLOCK_REPOSITORY_SECTION_FIELDS:
            assert field in section_data, f"Field '{field}' should be present in section"

        items = section_data["items"]
        assert isinstance(items, (dict, list)), "landing.block.getrepository section items should be dict or list"

        if isinstance(items, dict):
            iterable_items = items.items()
        else:
            iterable_items = enumerate(items)

        for item_key, item_data in iterable_items:
            if isinstance(items, dict):
                assert isinstance(item_key, str), "landing.block.getrepository block code should be str"
            assert isinstance(item_data, dict), "landing.block.getrepository block item should be dict"
            for field in _BLOCK_REPOSITORY_ITEM_FIELDS:
                assert field in item_data, f"Field '{field}' should be present in block item"
