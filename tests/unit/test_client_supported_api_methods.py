import pytest

from b24pysdk.client import Client
from tests.unit.examples import TOKEN_MOCK

pytestmark = [
    pytest.mark.unit,
]


def test_get_supported_api_methods_smoke():
    methods = Client(TOKEN_MOCK).get_supported_api_methods()

    assert methods
