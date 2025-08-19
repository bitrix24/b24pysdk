from typing import ClassVar, Dict, Text

import requests

from .._config import Config
from ..error import (
	BitrixAPIInsufficientScope,
	BitrixAPIInvalidRequest,
	BitrixOAuthInsufficientScope,
	BitrixOAuthInvalidRequest,
	BitrixOAuthRequestError,
	BitrixOAuthTimeout,
)
from ..utils.types import JSONDict, Timeout
from .bitrix_app import BitrixApp
from .functions.parse_response import parse_response


class OAuthRequester:
	""""""

	URL: ClassVar[Text] = "https://oauth.bitrix.info/oauth/token/"
	HEADERS: ClassVar[Dict] = {"Content-Type": "application/x-www-form-urlencoded"}

	def __init__(
		self,
		bitrix_app: BitrixApp,
		timeout: Timeout = None,
	):
		self._config = Config()
		self._bitrix_app = bitrix_app
		self._timeout = timeout or self._config.default_timeout

	def _get(self, params: JSONDict) -> JSONDict:
		""""""

		try:
			response = requests.get(self.URL, params=params, headers=self.HEADERS, timeout=self._timeout)
			return parse_response(response)

		except requests.Timeout as error:
			raise BitrixOAuthTimeout(timeout=self._timeout, original_error=error) from error

		except requests.RequestException as error:
			raise BitrixOAuthRequestError(original_error=error) from error

		except BitrixAPIInvalidRequest as error:
			raise BitrixOAuthInvalidRequest(response=error.response, json_response=error.json_response) from error

		except BitrixAPIInsufficientScope as error:
			raise BitrixOAuthInsufficientScope(response=error.response, json_response=error.json_response) from error

	def authorize(self, code: Text) -> JSONDict:
		""""""

		params = {
			"grant_type": "authorization_code",
			"client_id": self._bitrix_app.client_id,
			"client_secret": self._bitrix_app.client_secret,
			"code": code,
		}

		return self._get(params=params)

	def refresh(self, refresh_token: Text) -> JSONDict:
		""""""

		params = {
			"grant_type": "refresh_token",
			"client_id": self._bitrix_app.client_id,
			"client_secret": self._bitrix_app.client_secret,
			"refresh_token": refresh_token,
		}

		return self._get(params=params)
