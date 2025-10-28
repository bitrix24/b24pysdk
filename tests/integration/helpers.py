import os
from typing import Optional, Text
from urllib.parse import urlparse

from b24pysdk import BitrixApp, BitrixToken, BitrixWebhook, Client
from b24pysdk.bitrix_api.responses import BitrixAPIResponse

WEBHOOK_PARTS_COUNT = 2


class MissingCredentials(RuntimeError):
    pass


def _normalize_domain(raw: str) -> str:
    raw = raw.strip()
    parsed = urlparse(raw)
    host = parsed.netloc or raw
    host = host.lstrip("/")
    if "/" in host:
        host = host.split("/")[0]
    return host


def _validate_domain(domain: str) -> str:
    if not domain:
        raise MissingCredentials("B24_DOMAIN is required")
    if "://" in domain:
        raise MissingCredentials("B24_DOMAIN must be a host like 'example.bitrix24.ru' (no scheme)")
    if "/" in domain:
        raise MissingCredentials("B24_DOMAIN must not contain slashes; use only the host name")
    return domain


def _normalize_webhook(raw: str) -> str:
    return (raw or "").strip().strip("/")


def _validate_webhook(webhook: str) -> str:
    if not webhook:
        raise MissingCredentials("B24_WEBHOOK is required for webhook-based tests")
    parts = webhook.split("/")
    if len(parts) != WEBHOOK_PARTS_COUNT or not parts[0].isdigit():
        raise MissingCredentials("B24_WEBHOOK must be in format 'user_id/hook_key'")
    return webhook


def make_client_from_webhook() -> Client:
    """Construct a Client using an incoming webhook.

    Required env vars:
    - B24_DOMAIN: portal domain, e.g. example.bitrix24.ru (without scheme)
    - B24_WEBHOOK: webhook string in format "<user_id>/<hook_key>"
    """
    domain_raw = os.getenv("B24_DOMAIN", "")
    webhook_raw = os.getenv("B24_WEBHOOK", "")
    domain = _validate_domain(_normalize_domain(domain_raw))
    webhook = _validate_webhook(_normalize_webhook(webhook_raw))
    token = BitrixWebhook(domain=domain, auth_token=webhook)
    return Client(token)


def make_client_from_oauth(*, auto_refresh: bool = True) -> Client:
    """Construct a Client using OAuth application credentials and tokens.

    Required env vars:
    - B24_DOMAIN
    - B24_CLIENT_ID
    - B24_CLIENT_SECRET
    - B24_ACCESS_TOKEN
    - B24_REFRESH_TOKEN (optional for tests that don't refresh)
    """
    domain_raw = os.getenv("B24_DOMAIN", "")
    client_id = os.getenv("B24_CLIENT_ID")
    client_secret = os.getenv("B24_CLIENT_SECRET")
    access_token = os.getenv("B24_ACCESS_TOKEN")
    refresh_token: Optional[str] = os.getenv("B24_REFRESH_TOKEN")
    if not all([domain_raw, client_id, client_secret, access_token]):
        raise MissingCredentials(
            "Set B24_DOMAIN, B24_CLIENT_ID, B24_CLIENT_SECRET, B24_ACCESS_TOKEN (and optionally B24_REFRESH_TOKEN)",
        )
    domain = _validate_domain(_normalize_domain(domain_raw))
    app = BitrixApp(client_id=client_id, client_secret=client_secret)
    token = BitrixToken(domain=domain, auth_token=access_token, refresh_token=refresh_token, bitrix_app=app)
    # Respect auto-refresh flag for scenarios where we want to avoid refresh
    token.AUTO_REFRESH = auto_refresh
    return Client(token)


def make_client_from_env(prefer: str = "webhook") -> Client:
    """Create a Client from environment.

    prefer: "webhook" or "oauth". If preferred creds are missing, try the other.
    """
    prefer = prefer.lower()
    errors = []
    if prefer == "webhook":
        try:
            return make_client_from_webhook()
        except MissingCredentials as e:
            errors.append(str(e))
        try:
            return make_client_from_oauth()
        except MissingCredentials as e:
            errors.append(str(e))
    else:
        try:
            return make_client_from_oauth()
        except MissingCredentials as e:
            errors.append(str(e))
        try:
            return make_client_from_webhook()
        except MissingCredentials as e:
            errors.append(str(e))
    raise MissingCredentials("; ".join(errors))


def call_method(
        client: Client,
        api_method: Text,
        *args,
        **kwargs,
) -> BitrixAPIResponse:
    """"""

    scope, *parts = api_method.split(".")

    obj = getattr(client, scope)

    for attr in parts:
        obj = getattr(obj, attr)

    return obj(*args, **kwargs).call()
