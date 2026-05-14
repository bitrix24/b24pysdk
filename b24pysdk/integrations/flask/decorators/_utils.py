from http import HTTPStatus

from flask import Response, jsonify

from b24pysdk.utils.types import JSONDict

__all__ = [
    "make_json_response",
]


def make_json_response(payload: JSONDict, status_code: HTTPStatus) -> Response:
    response = jsonify(payload)
    response.status_code = status_code
    return response
