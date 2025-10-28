import pytest
from _pytest.cacheprovider import Cache
from _pytest.fixtures import SubRequest

from b24pysdk import Client
from tests.integration.helpers import make_client_from_env


@pytest.fixture(scope="session")
def bitrix_client(request: SubRequest) -> Client:
    """"""
    client_type = getattr(request, "param", "webhook")
    return make_client_from_env(prefer=client_type)


@pytest.fixture(scope="session")
def cache(request) -> Cache:
    """"""
    return request.config.cache
