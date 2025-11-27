import json
from pathlib import Path
from typing import Annotated, Literal, Text

from b24pysdk import BitrixApp, BitrixToken, BitrixWebhook, Client
from b24pysdk.bitrix_api.events import OAuthTokenRenewedEvent

from ..env_config import EnvConfig
from ..error import MissingCredentials

env_config = EnvConfig()

_CURRENT_DIR_PATH: Path = Path(__file__).parent
_OAUTH_FILE_PATH: Path = _CURRENT_DIR_PATH.parent / "oauth_data.json"


def _save_token_to_oauth_json(event: OAuthTokenRenewedEvent):
    oauth_token = event.renewed_oauth_token.oauth_token

    with Path.open(_OAUTH_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(
            oauth_token.to_dict(),
            file,
            ensure_ascii=False,
            indent=4,
            default=str,
        )


def _make_client_from_webhook() -> Client:
    if not env_config.are_webhook_credentials_available:
        raise MissingCredentials(
            "Webhook requires: 'B24_DOMAIN' and 'B24_WEBHOOK'",
        )

    webhook_token = BitrixWebhook(
        domain=env_config.domain,
        auth_token=env_config.webhook_token,
    )

    return Client(webhook_token)


def _make_client_from_oauth() -> Client:
    if not env_config.are_oauth_credentials_available:
        raise MissingCredentials(
            "OAuth requires: 'B24_DOMAIN', 'B24_CLIENT_ID', 'B24_CLIENT_SECRET', 'B24_ACCESS_TOKEN' and 'B24_REFRESH_TOKEN'",
        )

    bitrix_app = BitrixApp(
        client_id=env_config.client_id,
        client_secret=env_config.client_secret,
    )

    bitrix_token = BitrixToken(
        domain=env_config.domain,
        auth_token=env_config.access_token,
        refresh_token=env_config.refresh_token,
        bitrix_app=bitrix_app,
    )

    bitrix_token.oauth_token_renewed_signal.connect(_save_token_to_oauth_json)

    return Client(bitrix_token)


def make_client_from_env(auth_type: Annotated[Text, Literal["webhook", "oauth"]]) -> Client:
    if auth_type == "webhook":
        return _make_client_from_webhook()
    elif auth_type == "oauth":
        return _make_client_from_oauth()
    else:
        raise ValueError(f"Incorrect 'auth_type': {auth_type}")
