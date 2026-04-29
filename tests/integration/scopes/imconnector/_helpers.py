from b24pysdk.api.responses import BitrixAPIResponse
from b24pysdk.client import BaseClient


def get_active_open_line_id(bitrix_client: BaseClient) -> int:
    bitrix_response = bitrix_client.imopenlines.config.list.get(
        params={
            "select": ["ID", "ACTIVE"],
            "order": {"ID": "ASC"},
            "filter": {"ACTIVE": "Y"},
            "limit": 1,
            "offset": 0,
        },
    ).response

    assert isinstance(bitrix_response, BitrixAPIResponse)

    result = bitrix_response.result
    lines: list[dict] = []

    if isinstance(result, list):
        lines = [line for line in result if isinstance(line, dict)]
    elif isinstance(result, dict):
        for key in ("items", "ITEMS", "configs", "CONFIGS", "result"):
            value = result.get(key)
            if isinstance(value, list):
                lines = [line for line in value if isinstance(line, dict)]
                break

    assert lines, "No active open lines found for imconnector tests"

    line_id = lines[0].get("ID", lines[0].get("id"))
    if isinstance(line_id, str) and line_id.isdigit():
        line_id = int(line_id)

    assert isinstance(line_id, int), "Open line ID should be int"
    assert line_id > 0, "Open line ID should be positive"

    return line_id
