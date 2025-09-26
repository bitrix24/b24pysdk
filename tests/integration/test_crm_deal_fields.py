import os

import pytest

from .helpers import MissingCredentials, make_client_from_env


@pytest.mark.integration
def test_crm_deal_fields_real():
    """Call crm.deal.fields on a real Bitrix24 REST API.

    Uses webhook or OAuth credentials from the environment and skips if none are set.
    """
    try:
        client = make_client_from_env(prefer=os.getenv("B24_PREFER", "webhook"))
    except MissingCredentials:
        pytest.skip("No Bitrix24 credentials in environment; skipping integration test")

    resp = client.crm.deal.fields()
    fields = resp.result

    assert isinstance(fields, dict)
    # Common deal fields expected across portals
    for key in ("ID", "TITLE"):
        assert key in fields
