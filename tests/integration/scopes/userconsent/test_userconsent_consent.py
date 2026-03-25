from typing import Optional

import pytest

from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import BITRIX_PORTAL_OWNER_ID

pytestmark = [
    pytest.mark.integration,
    pytest.mark.userconsent,
    pytest.mark.userconsent_consent,
]


@pytest.mark.oauth_only
def test_add(bitrix_client: BaseClient):
    """"""

    agreements_response = bitrix_client.userconsent.agreement.list().response

    assert isinstance(agreements_response, BitrixAPIResponse)
    assert isinstance(agreements_response.result, list), "userconsent.agreement.list result should be a list"

    agreement_id: Optional[int] = None

    for agreement in agreements_response.result:
        if not isinstance(agreement, dict):
            continue

        current_agreement_id = agreement.get("ID")
        if isinstance(current_agreement_id, int):
            agreement_id = current_agreement_id
            break

        if isinstance(current_agreement_id, str) and current_agreement_id.isdigit():
            agreement_id = int(current_agreement_id)
            break

    if agreement_id is None:
        pytest.skip("No agreement found for userconsent.consent.add test")

    bitrix_response = bitrix_client.userconsent.consent.add(
        agreement_id=agreement_id,
        ip="127.0.0.1",
        user_id=BITRIX_PORTAL_OWNER_ID,
        url="https://example.com/consent",
        origin_id="sdk_consent",
        originator_id="sdk_originator",
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "userconsent.consent.add result should be int"
    assert bitrix_response.result > 0, "userconsent.consent.add should return a positive ID"
