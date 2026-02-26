from abc import ABC
from http import HTTPStatus
from typing import ClassVar

import requests

__all__ = [
    "HTTPResponse",
    "HTTPResponseBadRequest",
    "HTTPResponseForbidden",
    "HTTPResponseFound",
    "HTTPResponseInternalServerError",
    "HTTPResponseMethodNotAllowed",
    "HTTPResponseNotFound",
    "HTTPResponseOK",
    "HTTPResponseServiceUnavailable",
    "HTTPResponseTooManyRequests",
    "HTTPResponseUnauthorized",
]


class HTTPResponse(ABC):
    """"""

    STATUS_CODE: ClassVar[HTTPStatus] = NotImplemented

    response: requests.Response

    @property
    def status_code(self) -> int:
        """"""
        return self.response.status_code


class HTTPResponseOK(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.OK


class HTTPResponseFound(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.FOUND


class HTTPResponseBadRequest(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.BAD_REQUEST


class HTTPResponseUnauthorized(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.UNAUTHORIZED


class HTTPResponseForbidden(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.FORBIDDEN


class HTTPResponseNotFound(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.NOT_FOUND


class HTTPResponseMethodNotAllowed(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.METHOD_NOT_ALLOWED


class HTTPResponseTooManyRequests(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.TOO_MANY_REQUESTS


class HTTPResponseInternalServerError(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.INTERNAL_SERVER_ERROR


class HTTPResponseServiceUnavailable(HTTPResponse):
    """"""
    STATUS_CODE = HTTPStatus.SERVICE_UNAVAILABLE
