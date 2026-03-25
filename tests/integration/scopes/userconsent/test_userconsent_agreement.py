from typing import Optional

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.userconsent,
    pytest.mark.userconsent_agreement,
]


@pytest.mark.oauth_only
def test_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.userconsent.agreement.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "userconsent.agreement.list result should be a list"

    agreements = bitrix_response.result
    for agreement in agreements:
        assert isinstance(agreement, dict), "Each agreement should be a dict"
        assert "ID" in agreement, "Field 'ID' should be present in userconsent.agreement.list result"


@pytest.mark.oauth_only
def test_text(bitrix_client: BaseClient):
    """"""

    list_response = bitrix_client.userconsent.agreement.list().response

    assert isinstance(list_response, BitrixAPIResponse)
    assert isinstance(list_response.result, list), "userconsent.agreement.list result should be a list"

    agreements = list_response.result
    first_agreement_id: Optional[int] = None

    for agreement in agreements:
        if isinstance(agreement, dict):
            agreement_id = agreement.get("ID")
            if isinstance(agreement_id, str) and agreement_id.isdigit():
                first_agreement_id = int(agreement_id)
                break
            if isinstance(agreement_id, int):
                first_agreement_id = agreement_id
                break

    if first_agreement_id is None:
        pytest.skip("No user consent agreements available for userconsent.agreement.text test")

    text_response = bitrix_client.userconsent.agreement.text(bitrix_id=first_agreement_id).response

    assert isinstance(text_response, BitrixAPIResponse)
    assert isinstance(text_response.result, dict), "userconsent.agreement.text result should be a dict"

    agreement_text_data = text_response.result
    assert len(agreement_text_data) > 0, "userconsent.agreement.text result should not be empty"
