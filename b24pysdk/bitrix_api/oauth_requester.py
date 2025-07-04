from typing import Text

import requests

from ..error import BitrixOAuthTimeout, BitrixOAuthRequestError
from ..utils.types import JSONDict, Timeout
from .bitrix_app import BitrixApp
from .config import SdkConfig
from .functions.parse_response import parse_response


class OAuthRequester:
	""""""

	URL = "https://oauth.bitrix.info/oauth/token/"
	HEADERS = {"Content-Type": "application/x-www-form-urlencoded"}

	def __init__(
		self,
		bitrix_app: BitrixApp,
		timeout: Timeout = None,
	):
		self._config = SdkConfig()
		self.bitrix_app = bitrix_app
		self._timeout = timeout or self._config.default_timeout

	def _get(self, params: JSONDict) -> JSONDict:
		""""""

		try:
			response = requests.get(self.URL, params=params, headers=self.HEADERS)
			return parse_response(response)

		except requests.Timeout as error:
			raise BitrixOAuthTimeout(timeout=self._timeout, original_error=error) from error

		except requests.RequestException as error:
			raise BitrixOAuthRequestError(original_error=error) from error

	def authenticate(self, code: Text) -> JSONDict:
		""""""

		params = {
			"grant_type": "authorization_code",
			"client_id": self.bitrix_app.client_id,
			"client_secret": self.bitrix_app.client_secret,
			"code": code,
		}

		return self._get(params=params)

	def refresh(self, refresh_token: Text) -> JSONDict:
		""""""

		params = {
			"grant_type": "refresh_token",
			"client_id": self.bitrix_app.client_id,
			"client_secret": self.bitrix_app.client_secret,
			"refresh_token": refresh_token,
		}

		return self._get(params=params)
