import pytest
from _pytest.cacheprovider import Cache
from _pytest.fixtures import SubRequest

from b24pysdk import Client
from tests.integration.helpers import make_client_from_env

from .env_config import EnvConfig
from .error import MissingCredentials

env_config = EnvConfig()


@pytest.fixture(scope="session")
def bitrix_client(request: SubRequest) -> Client:
    auth_type = getattr(request, "param", "webhook")
    try:
        return make_client_from_env(auth_type=auth_type)
    except MissingCredentials:
        pytest.skip("Missing credentials for this auth type")


@pytest.fixture(scope="session")
def cache(request: pytest.FixtureRequest) -> Cache:
    return request.config.cache


def pytest_generate_tests(metafunc: pytest.Metafunc):
    if "bitrix_client" in metafunc.fixturenames:
        if "oauth_only" in metafunc.definition.keywords:
            clients = [
                pytest.param("oauth", id="oauth", marks=pytest.mark.skipif(
                    not env_config.are_oauth_credentials_available,
                    reason="Missing OAuth credentials",
                )),
            ]
        elif "webhook_only" in metafunc.definition.keywords:
            clients = [
                pytest.param("webhook", id="webhook", marks=pytest.mark.skipif(
                    not env_config.are_webhook_credentials_available,
                    reason="Missing webhook credentials",
                )),
            ]
        else:
            clients = [
                pytest.param("webhook", id="webhook"),
                pytest.param("oauth", id="oauth", marks=pytest.mark.skipif(
                    not env_config.are_oauth_credentials_available,
                    reason="Missing OAuth credentials",
                )),
            ]
        metafunc.parametrize("bitrix_client", clients, indirect=True)


def pytest_runtest_setup(item: pytest.Item):
    if "oauth_only" in item.keywords and not env_config.are_oauth_credentials_available:
        pytest.skip("Skipping test because OAuth credentials are missing")
