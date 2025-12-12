import json
import re
from datetime import datetime
from pathlib import Path
from typing import Annotated, Literal, Optional, Text

from environs import Env

from b24pysdk import Config
from b24pysdk.log import StreamLogger

from .constants import ENV_FILE, OAUTH_DATA_FILE, AuthType
from .error import InvalidCredentials

__all__ = [
    "EnvConfig",
]

Config().configure(
    logger=StreamLogger(),
)


class EnvConfig:
    """"""

    _instance: Optional["EnvConfig"] = None

    __slots__ = (
        "access_token",
        "client_id",
        "client_secret",
        "domain",
        "expires",
        "expires_in",
        "prefer_auth_type",
        "refresh_token",
        "webhook_token",
    )

    access_token: Text
    client_id: Text
    client_secret: Text
    domain: Text
    expires: Optional[datetime]
    expires_in: Optional[datetime]
    prefer_auth_type: AuthType
    refresh_token: Text
    webhook_token: Text

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
            self,
            env_file: Text = ENV_FILE,
            oauth_data_file: Text = OAUTH_DATA_FILE,
    ):
        env = Env()
        env_file_path = Path(env_file)

        if env_file_path.exists():
            env.read_env(env_file_path)

        self.domain = self._validate_domain(env.str("B24_DOMAIN", default=""))
        self.webhook_token = self._validate_webhook_token(env.str("B24_WEBHOOK", default=""))
        self.client_id = self._validate_credential(env.str("B24_CLIENT_ID", default=""), name="B24_CLIENT_ID")
        self.client_secret = self._validate_credential(env.str("B24_CLIENT_SECRET", default=""), name="B24_CLIENT_SECRET")
        self.access_token = self._validate_credential(env.str("B24_ACCESS_TOKEN", default=""), name="B24_ACCESS_TOKEN")
        self.refresh_token = self._validate_credential(env.str("B24_REFRESH_TOKEN", default=""), name="B24_REFRESH_TOKEN")
        self.expires = self._validate_expires(env.str("B24_EXPIRES", default=None))
        self.expires_in = self._validate_expires_in(env.int("B24_EXPIRES_IN", default=None))
        self.prefer_auth_type = self._validate_prefer_auth_type(env.str("B24_PREFER_AUTH_TYPE", default=""))

        oauth_data_file_path = Path(oauth_data_file)

        if oauth_data_file_path.exists():
            with Path.open(oauth_data_file_path, "r", encoding="utf-8") as file:
                oauth_data = json.load(file)

                access_token = self._validate_credential(oauth_data.get("access_token"), name="access_token")
                refresh_token = self._validate_credential(oauth_data.get("refresh_token"), name="refresh_token")
                expires = self._validate_expires(oauth_data.get("expires"))
                expires_in = self._validate_expires_in(oauth_data.get("expires_in"))

                if access_token and refresh_token:
                    self.access_token = access_token
                    self.refresh_token = refresh_token
                    self.expires = expires
                    self.expires_in = expires_in

                    if expires and Config().get_local_datetime() > expires:
                        Config().logger.warning("The access token has expired, use the application_bridge to refresh the OAuth token.")

    @staticmethod
    def _validate_domain(domain: Text) -> Text:
        if not domain:
            return domain

        if not (isinstance(domain, str) and re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain)):
            raise InvalidCredentials(f"Invalid 'B24_DOMAIN' format: {domain!r}")

        return domain

    @staticmethod
    def _validate_webhook_token(webhook_token: Text) -> Text:
        if not webhook_token:
            return webhook_token

        webhook_token = webhook_token.strip().strip("/")

        if not (isinstance(webhook_token, str) and re.match(r"^\d+/[a-zA-Z0-9]+$", webhook_token)):
            raise InvalidCredentials(f"'B24_WEBHOOK' must be in format 'user_id/hook_key': {webhook_token!r}")

        return webhook_token

    @staticmethod
    def _validate_credential(credential: Text, name: Text) -> Text:
        if not credential:
            return credential

        if not (isinstance(credential, str) and re.match(r"^[a-zA-Z0-9.]+$", credential)):
            raise InvalidCredentials(f"Invalid {name!r} format: {credential!r}")

        return credential

    @staticmethod
    def _validate_prefer_auth_type(prefer_auth_type: Annotated[Text, Literal["", "oauth", "webhook"]]) -> AuthType:
        try:
            return AuthType(prefer_auth_type)
        except ValueError as error:
            raise InvalidCredentials(f"Invalid 'B24_PREFER_AUTH_TYPE' format: {prefer_auth_type!r}") from error

    @staticmethod
    def _validate_expires(expires:  Optional[Text]) -> Optional[datetime]:
        if not expires:
            return None

        if not isinstance(expires, str):
            raise InvalidCredentials(f"'expires' must be a string, got {type(expires).__name__!r}")

        try:
            expires_dt = datetime.fromisoformat(expires)
        except ValueError as error:
            raise InvalidCredentials(
                f"'expires' must be in ISO 8601 format (e.g. '2025-11-28 21:09:16+03:00'), got {expires!r}",
            ) from error

        return expires_dt

    @staticmethod
    def _validate_expires_in(expires_in: Optional[int]) -> Optional[int]:
        if expires_in is None:
            return None

        if type(expires_in) is not int:
            raise InvalidCredentials(f"'expires_in' must be an integer, got {type(expires_in).__name__!r}")

        if expires_in <= 0:
            raise InvalidCredentials(f"'expires_in' must be a positive integer, got {expires_in!r}")

        return expires_in

    @property
    def are_webhook_credentials_available(self) -> bool:
        """"""
        return all((
            self.prefer_auth_type != AuthType.OAUTH,
            self.domain,
            self.webhook_token,
        ))

    @property
    def are_oauth_credentials_available(self) -> bool:
        """"""
        return all((
            self.prefer_auth_type != AuthType.WEBHOOK,
            self.domain,
            self.access_token,
            self.refresh_token,
            self.client_id,
            self.client_secret,
        ))
