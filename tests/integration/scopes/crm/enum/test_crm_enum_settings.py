from typing import Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIValuesResponse
from b24pysdk.client import BaseClient
from b24pysdk.schemas.crm.enum import CRMEnumItem

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.crm,
    pytest.mark.crm_enum,
    pytest.mark.crm_enum_settings,
]

_EXPECTED_MODE_IDS: Tuple[int, ...] = (1, 2)


def test_crm_enum_settings_mode(bitrix_client: BaseClient):
    """Test retrieving CRM operation mode enum values."""

    bitrix_response = bitrix_client.crm.enum.settings.mode().response

    assert isinstance(bitrix_response, BitrixAPIValuesResponse)

    modes = bitrix_response.values

    assert isinstance(modes, list), "CRM enum settings mode values should be a list"
    assert modes, "CRM enum settings mode values should not be empty"

    mode_ids = {mode.bitrix_id for mode in modes}

    for expected_mode_id in _EXPECTED_MODE_IDS:
        assert expected_mode_id in mode_ids, f"CRM mode ID {expected_mode_id!r} should be present"

    for mode in modes:
        assert isinstance(mode, CRMEnumItem), "CRM enum settings mode item should be CRMEnumItem"
        assert isinstance(mode.bitrix_id, int), "CRMEnumItem.bitrix_id should be an int"
        assert isinstance(mode.name, str), "CRMEnumItem.name should be a str"
        assert mode.symbol_code is None or isinstance(mode.symbol_code, str), "CRMEnumItem.symbol_code should be a str or None"
        assert mode.symbol_code_short is None or isinstance(mode.symbol_code_short, str), "CRMEnumItem.symbol_code_short should be a str or None"
