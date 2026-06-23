import pytest

from b24pysdk.api.responses import BitrixAPIValueResponse
from b24pysdk.client import BaseClient
from b24pysdk.constants import B24AppStatus
from b24pysdk.schemas.app import AppInfoApplication, AppInfoWebhook

pytestmark = [
    pytest.mark.integration,
    pytest.mark.scopes,
    pytest.mark.app,
]


def test_app_info(bitrix_client: BaseClient):
    """"""

    bitrix_response = bitrix_client.app.info().response

    assert isinstance(bitrix_response, BitrixAPIValueResponse)

    app_info = bitrix_response.value

    assert isinstance(app_info, (AppInfoApplication, AppInfoWebhook)), "App info value should be AppInfoApplication or AppInfoWebhook"
    assert isinstance(app_info.license, str), "AppInfo.license should be a str"

    if isinstance(app_info, AppInfoApplication):
        assert isinstance(app_info.bitrix_id, int), "AppInfoApplication.bitrix_id should be an int"
        assert isinstance(app_info.code, str), "AppInfoApplication.code should be a str"
        assert isinstance(app_info.version, int), "AppInfoApplication.version should be an int"
        assert isinstance(app_info.status, B24AppStatus), "AppInfoApplication.status should be B24AppStatus"
        assert isinstance(app_info.installed, bool), "AppInfoApplication.installed should be a bool"
        assert isinstance(app_info.payment_expired, bool), "AppInfoApplication.payment_expired should be a bool"
        assert app_info.days is None or isinstance(app_info.days, int), "AppInfoApplication.days should be an int or None"
        assert isinstance(app_info.language_id, str), "AppInfoApplication.language_id should be a str"
        assert isinstance(app_info.license_type, str), "AppInfoApplication.license_type should be a str"
        assert isinstance(app_info.license_family, str), "AppInfoApplication.license_family should be a str"

    else:
        assert isinstance(app_info.scope, list), "AppInfoWebhook.scope should be a list"

        for scope in app_info.scope:
            assert isinstance(scope, str), "AppInfoWebhook.scope item should be a str"
