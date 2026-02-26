from typing import Text, Tuple

import pytest

from b24pysdk.api.responses import BitrixAPIListResponse, BitrixAPIResponse
from b24pysdk.client import BaseClient

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scope,
]

_SCOPES: Tuple[Text, ...] = ("booking", "biconnector", "telephony", "call", "timeman", "task", "tasks_extended", "log", "sonet_group", "sign.b2e", "sale", "cashbox", "delivery", "pay_system", "rpa", "placement", "user", "user_brief",
                             "user_basic", "user.userfield", "entity", "pull", "pull_channel", "mobile", "messageservice",  "mailservice", "lists", "landing", "landing_cloud", "department", "contact_center", "crm", "imopenlines",
                             "imbot", "im", "humanresources.hcmlink", "forum", "documentgenerator", "disk", "catalog", "calendar", "bizproc", "ai_admin", "userconsent", "rating", "smile", "userfieldconfig", "baas", "calendarmobile",
                             "catalogmobile", "iblock", "im.import", "imconnector", "intranet", "main", "notifications", "appform", "configuration.import", "rest", "salescenter", "socialnetwork", "tasks", "tasksmobile", "vote")


def test_scope(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.scope(full=True).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "Scopes should be a list of strings"

    scopes = bitrix_response.result

    for scope in _SCOPES:
        assert scope in scopes, f"Scope {scope!r} should be present"


def test_scope_as_list(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.scope(full=True).as_list().response

    assert isinstance(bitrix_response, BitrixAPIListResponse)
    assert isinstance(bitrix_response.result, list), "Scopes should be a list of strings"

    scopes = bitrix_response.result

    for scope in _SCOPES:
        assert scope in scopes, f"Scope {scope!r} should be present"
