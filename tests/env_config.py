import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Text

from environs import Env

from b24pysdk import Config

from .constants import ENV_FILE, OAUTH_DATA_FILE, AuthType
from .error import InvalidCredentials

__all__ = [
    "EnvConfig",
]


class EnvConfig:
    """"""

    _instance: Optional["EnvConfig"] = None

    __slots__ = (
        "access_token",
        "client_id",
        "client_secret",
        "domain",
        "prefer_auth_type",
        "refresh_token",
        "webhook_token",
    )

    access_token: Text
    client_id: Text
    client_secret: Text
    domain: Text
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
        self.prefer_auth_type = self._validate_prefer_auth_type(env.str("B24_PREFER_AUTH_TYPE", default=""))

        oauth_data_file_path = Path(oauth_data_file)

        if oauth_data_file_path.exists():
            with Path.open(oauth_data_file_path, "r", encoding="utf-8") as file:
                oauth_data = json.load(file)

                access_token = oauth_data.get("access_token")
                refresh_token = oauth_data.get("refresh_token")
                expires = oauth_data.get("expires")

                if access_token and refresh_token:
                    self.access_token = self._validate_credential(access_token, name="B24_ACCESS_TOKEN")
                    self.refresh_token = self._validate_credential(refresh_token, name="B24_REFRESH_TOKEN")

                if expires:
                    expires_dt = datetime.fromisoformat(expires)

                    if datetime.now(tz=Config().tzinfo) > expires_dt:
                        Config().logger.warning("The access token has expired, use the application_bridge to refresh the OAuth.")

    @staticmethod
    def _validate_domain(domain: Text) -> Text:
        if not domain:
            return domain

        if not re.match(r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", domain):
            raise InvalidCredentials(f"Invalid 'B24_DOMAIN' format: {domain!r}")

        return domain

    @staticmethod
    def _validate_webhook_token(webhook_token: Text) -> Text:
        if not webhook_token:
            return webhook_token

        webhook_token = webhook_token.strip().strip("/")

        if not re.match(r"^\d+/[a-zA-Z0-9]+$", webhook_token):
            raise InvalidCredentials(f"'B24_WEBHOOK' must be in format 'user_id/hook_key': {webhook_token!r}")

        return webhook_token

    @staticmethod
    def _validate_credential(credential: Text, name: Text) -> Text:
        if not credential:
            return credential

        if not re.match(r"^[a-zA-Z0-9.]+$", credential):
            raise InvalidCredentials(f"Invalid {name!r} format: {credential!r}")

        return credential

    @staticmethod
    def _validate_prefer_auth_type(prefer_auth_type: Text) -> AuthType:
        try:
            return AuthType(prefer_auth_type)
        except ValueError as error:
            raise InvalidCredentials(f"Invalid 'B24_PREFER_AUTH_TYPE' format: {prefer_auth_type!r}") from error

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
