"""
SimpleFIN client.

SimpleFIN's flow (it's "OAuth-adjacent" but simpler than full OAuth2):

1. The user gets a one-time "setup token" from a SimpleFIN bridge (e.g. by
   connecting their bank through the bridge's web UI).
2. The setup token is base64-encoded text that decodes to a one-time "claim URL".
3. We POST to that claim URL (no body needed). The response body is the
   permanent "access URL" — this contains embedded HTTP Basic Auth credentials,
   e.g. https://username:password@bridge.simplefin.org/simplefin
4. From then on, we use that access URL directly (with Basic Auth) to fetch
   accounts and transactions. There's no refresh token or expiry to manage —
   the access URL itself IS the long-lived credential, so guard it like a password.
"""

import time
import base64
import httpx

SIMPLEFIN_CLAIM_TIMEOUT = 10.0
SIMPLEFIN_REQUEST_TIMEOUT = 15.0


class SimpleFinError(Exception):
    pass


class RateLimiter:
    """
    Minimal client-side rate limiter: enforces a minimum gap between
    outgoing requests. SimpleFIN doesn't publish a hard rate limit, but
    self-throttling is good practice for any third-party API.
    """

    def __init__(self, min_interval_seconds: float = 1.0):
        self.min_interval = min_interval_seconds
        self._last_call = 0.0

    def wait(self):
        elapsed = time.monotonic() - self._last_call
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self._last_call = time.monotonic()


_rate_limiter = RateLimiter(min_interval_seconds=1.0)


def claim_setup_token(setup_token: str) -> str:
    """
    Exchange a one-time setup token for a permanent SimpleFIN access URL.
    Raises SimpleFinError on any failure.
    """
    try:
        claim_url = base64.b64decode(setup_token).decode("utf-8")
    except Exception as e:
        raise SimpleFinError(f"Invalid setup token: {e}")

    _rate_limiter.wait()

    try:
        response = httpx.post(claim_url, timeout=SIMPLEFIN_CLAIM_TIMEOUT)
    except httpx.RequestError as e:
        raise SimpleFinError(f"Network error claiming setup token: {e}")

    if response.status_code != 200:
        raise SimpleFinError(
            f"Failed to claim setup token: {response.status_code} {response.text}"
        )

    access_url = response.text.strip()
    if not access_url.startswith("http"):
        raise SimpleFinError("Unexpected response when claiming setup token")

    return access_url


def fetch_accounts(access_url: str, start_date: int | None = None) -> dict:
    """
    Fetch accounts (and their recent transactions) from SimpleFIN.

    start_date: optional Unix timestamp to limit how far back transactions go.
    """
    params = {}
    if start_date:
        params["start-date"] = start_date

    accounts_endpoint = f"{access_url}/accounts"
    response = _request_with_backoff(accounts_endpoint, params)
    return response.json()


def _request_with_backoff(url: str, params: dict, max_retries: int = 3) -> httpx.Response:
    """
    GET with exponential backoff on transient failures.

    - Respects Retry-After on 429 responses if present.
    - Retries on 5xx and network errors.
    - Does NOT retry on 4xx (besides 429) — those are our fault and retrying won't help.
    """
    delay = 1.0
    last_exception: Exception | None = None

    for attempt in range(max_retries):
        _rate_limiter.wait()

        try:
            response = httpx.get(url, params=params, timeout=SIMPLEFIN_REQUEST_TIMEOUT)
        except httpx.RequestError as e:
            last_exception = e
            time.sleep(delay)
            delay *= 2
            continue

        if response.status_code == 429:
            retry_after = float(response.headers.get("Retry-After", delay))
            time.sleep(retry_after)
            delay *= 2
            continue

        if response.status_code >= 500:
            time.sleep(delay)
            delay *= 2
            continue

        if response.status_code != 200:
            raise SimpleFinError(
                f"SimpleFIN request failed: {response.status_code} {response.text}"
            )

        return response

    raise SimpleFinError(
        f"SimpleFIN request failed after {max_retries} retries: {last_exception}"
    )
