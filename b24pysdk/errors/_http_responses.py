from abc import ABC
from http import HTTPStatus
from typing import ClassVar

import requests

__all__ = [
    "HTTPResponse",
    "HTTPResponseBadRequest",
    "HTTPResponseForbidden",
    "HTTPResponseFound",
    "HTTPResponseGone",
    "HTTPResponseInternalServerError",
    "HTTPResponseMethodNotAllowed",
    "HTTPResponseNotFound",
    "HTTPResponseOK",
    "HTTPResponseServiceUnavailable",
    "HTTPResponseTooManyRequests",
    "HTTPResponseUnauthorized",
]


class HTTPResponse(ABC):
    """
    Abstract base class representing a typed HTTP response.

    This class wraps a `requests.Response` object and provides
    a structured way to represent specific HTTP status codes
    through subclasses.
    """

    STATUS_CODE: ClassVar[HTTPStatus] = NotImplemented

    response: requests.Response

    @property
    def status_code(self) -> int:
        """
        Return the numeric HTTP status code of the response.

        Returns
        -------
        int
            HTTP status code from the underlying `requests.Response`.
        """
        return self.response.status_code


class HTTPResponseOK(HTTPResponse):
    """
    HTTP 200 OK response.

    Indicates that the request was successfully processed.
    """
    STATUS_CODE = HTTPStatus.OK


class HTTPResponseFound(HTTPResponse):
    """
    HTTP 302 Found response.

    Indicates that the requested resource temporarily resides
    under a different URI.
    """
    STATUS_CODE = HTTPStatus.FOUND


class HTTPResponseBadRequest(HTTPResponse):
    """
    HTTP 400 Bad Request response.

    Indicates that the server could not understand the request
    due to invalid syntax.
    """
    STATUS_CODE = HTTPStatus.BAD_REQUEST


class HTTPResponseUnauthorized(HTTPResponse):
    """
    HTTP 401 Unauthorized response.

    Indicates that authentication is required and has either
    not been provided or failed.
    """
    STATUS_CODE = HTTPStatus.UNAUTHORIZED


class HTTPResponseForbidden(HTTPResponse):
    """
    HTTP 403 Forbidden response.

    Indicates that the server understood the request but refuses
    to authorize it.
    """
    STATUS_CODE = HTTPStatus.FORBIDDEN


class HTTPResponseNotFound(HTTPResponse):
    """
    HTTP 404 Not Found response.

    Indicates that the requested resource could not be found
    on the server.
    """
    STATUS_CODE = HTTPStatus.NOT_FOUND


class HTTPResponseMethodNotAllowed(HTTPResponse):
    """
    HTTP 405 Method Not Allowed response.

    Indicates that the request method is not supported
    for the requested resource.
    """
    STATUS_CODE = HTTPStatus.METHOD_NOT_ALLOWED


class HTTPResponseGone(HTTPResponse):
    """
    HTTP 410 Gone response.

    Indicates that the requested resource is no longer available
    and will not be available again.
    """
    STATUS_CODE = HTTPStatus.GONE


class HTTPResponseTooManyRequests(HTTPResponse):
    """
    HTTP 429 Too Many Requests response.

    Indicates that the client has sent too many requests
    in a given amount of time (rate limiting).
    """
    STATUS_CODE = HTTPStatus.TOO_MANY_REQUESTS


class HTTPResponseInternalServerError(HTTPResponse):
    """
    HTTP 500 Internal Server Error response.

    Indicates that the server encountered an unexpected condition
    that prevented it from fulfilling the request.
    """
    STATUS_CODE = HTTPStatus.INTERNAL_SERVER_ERROR


class HTTPResponseServiceUnavailable(HTTPResponse):
    """
    HTTP 503 Service Unavailable response.

    Indicates that the server is currently unable to handle
    the request due to temporary overload or maintenance.
    """
    STATUS_CODE = HTTPStatus.SERVICE_UNAVAILABLE
