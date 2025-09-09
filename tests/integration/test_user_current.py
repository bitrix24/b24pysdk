import os

import pytest

from b24pysdk.error import BitrixAPIInsufficientScope, BitrixAPIUnauthorized
from tests.integration.helpers import MissingCredentials, make_client_from_env


@pytest.mark.integration
def test_user_current_real():
    """Hit Bitrix24 REST API (user.current) using webhook or OAuth credentials from env.

    Skips if neither set of credentials is available.
    """
    try:
    # Prefer webhook as it's simpler, fall back to OAuth if needed
        client = make_client_from_env(prefer=os.getenv("B24_PREFER", "webhook"))
    except MissingCredentials:
        pytest.skip("No Bitrix24 credentials in environment; skipping integration test")

    resp = client.user.current()
    # Deferred call: accessing result triggers the request/parse
    try:
        data = resp.result
    except BitrixAPIInsufficientScope:
        # Webhooks can lack scope for user.current on some portals; try OAuth if available.
        try:
            client = make_client_from_env(prefer="oauth")
        except MissingCredentials:
            pytest.skip("Webhook lacks scope for user.current and OAuth credentials are not provided")
        try:
            data = client.user.current().result
        except BitrixAPIUnauthorized:
            pytest.skip("OAuth tokens are invalid or app is not installed for user.current")

    # Basic shape assertions, tolerant across portals
    assert isinstance(data, dict)
    assert "ID" in data or "id" in data
    # Common fields often present
    for k in ("NAME", "EMAIL", "LAST_NAME"):
        if k in data:
            assert isinstance(data[k], (str, type(None)))
