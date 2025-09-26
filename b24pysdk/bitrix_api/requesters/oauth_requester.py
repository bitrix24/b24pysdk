from typing import Dict, Final, Optional, Text

import requests

from ...error import (
	BitrixAPIInsufficientScope,
	BitrixAPIInvalidRequest,
	BitrixOAuthInsufficientScope,
	BitrixOAuthInvalidRequest,
	BitrixOAuthRequestError,
	BitrixOAuthTimeout,
)
from ...utils.types import JSONDict, Number, Timeout
from ..bitrix_app import AbstractBitrixApp
from ..functions.parse_response import parse_response
from ._base_requester import BaseRequester


class OAuthRequester(BaseRequester):
	""""""

	_URL: Final[Text] = "https://oauth.bitrix.info/oauth/token/"
	_HEADERS: Final[Dict] = {"Content-Type": "application/x-www-form-urlencoded"}

	__slots__ = ("_bitrix_app",)

	_bitrix_app: AbstractBitrixApp

	def __init__(
		self,
		bitrix_app: AbstractBitrixApp,
		timeout: Timeout = None,
		max_retries: Optional[int] = None,
		initial_retry_delay: Optional[Number] = None,
		retry_delay_increment: Optional[Number] = None,
	):
		super().__init__(
			timeout=timeout,
			max_retries=max_retries,
			initial_retry_delay=initial_retry_delay,
			retry_delay_increment=retry_delay_increment,
		)
		self._bitrix_app = bitrix_app

	@property
	def _headers(self) -> Dict:
		""""""
		return self._get_default_headers() | self._HEADERS

	def _request(self, params: JSONDict) -> requests.Response:
		return requests.get(
			url=self._URL,
			params=params,
			headers=self._headers,
			timeout=self._timeout,
		)

	def _get(self, params: JSONDict) -> requests.Response:
		""""""

		try:
			return self._request_with_retries(params=params)

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

		return parse_response(self._get(params=params))

	def refresh(self, refresh_token: Text) -> JSONDict:
		""""""

		params = {
			"grant_type": "refresh_token",
			"client_id": self._bitrix_app.client_id,
			"client_secret": self._bitrix_app.client_secret,
			"refresh_token": refresh_token,
		}

		return parse_response(self._get(params=params))
