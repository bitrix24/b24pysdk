from http import HTTPStatus
from typing import Any

from flask import jsonify

__all__ = [
    "_make_json_response",
]


def _make_json_response(payload: dict[str, Any], status_code: HTTPStatus):
    response = jsonify(payload)
    response.status_code = status_code
    return response
