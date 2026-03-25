import pytest
from _pytest.cacheprovider import Cache

from b24pysdk import Config
from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient

from ....constants import SDK_NAME

pytestmark = [
    pytest.mark.integration,
    pytest.mark.ai_admin,
    pytest.mark.ai_admin_engine,
]

_COMPLETIONS_URL: str = "https://example.com"
_ENGINE_FIELDS = ("CODE", "NAME")


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_ai_admin_engine_register")
def test_register(bitrix_client: BaseClient, cache: Cache):
    """"""

    engine_code = f"sdk_engine_{int(Config().get_local_datetime().timestamp() * (10 ** 6))}"
    engine_name = f"{SDK_NAME} AI Engine"

    bitrix_response = bitrix_client.ai.engine.register(
        name=engine_name,
        code=engine_code,
        category="text",
        completions_url=_COMPLETIONS_URL,
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, int), "ai.engine.register should return engine ID as int"

    engine_id = bitrix_response.result
    assert engine_id > 0, "ai.engine.register should return positive ID"

    cache.set("ai_admin_engine_code", engine_code)


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_ai_admin_engine_list", depends=["test_ai_admin_engine_register"])
def test_list(bitrix_client: BaseClient, cache: Cache):
    """"""

    engine_code = cache.get("ai_admin_engine_code", None)
    assert isinstance(engine_code, str), "ai engine code should be cached"

    bitrix_response = bitrix_client.ai.engine.list().response

    assert isinstance(bitrix_response, BitrixAPIResponse)
    assert isinstance(bitrix_response.result, list), "ai.engine.list result should be a list"

    engines = bitrix_response.result

    for engine in engines:
        assert isinstance(engine, dict), "Each engine should be a dict"

        if "CODE" in engine and "NAME" in engine:
            for field in _ENGINE_FIELDS:
                assert field in engine, f"Field '{field}' should be present"
        else:
            assert "code" in engine, "Field 'code' should be present"
            assert "name" in engine, "Field 'name' should be present"

    assert any(
        engine.get("CODE") == engine_code or engine.get("code") == engine_code
        for engine in engines
    ), "Registered AI engine should be present in ai.engine.list"


@pytest.mark.oauth_only
@pytest.mark.dependency(name="test_ai_admin_engine_unregister", depends=["test_ai_admin_engine_register"])
def test_unregister(bitrix_client: BaseClient, cache: Cache):
    """"""

    engine_code = cache.get("ai_admin_engine_code", None)
    assert isinstance(engine_code, str), "ai engine code should be cached"

    bitrix_response = bitrix_client.ai.engine.unregister(code=engine_code).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    is_unregistered = bitrix_response.result
    assert is_unregistered is True, "ai.engine.unregister should return True"
