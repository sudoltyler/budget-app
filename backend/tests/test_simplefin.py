import base64
from unittest.mock import patch, MagicMock

from simplefin_app.simplefin import claim_setup_token, SimpleFinError


def test_claim_setup_token_success():
    claim_url = "https://bridge.simplefin.org/claim/abc123"
    setup_token = base64.b64encode(claim_url.encode()).decode()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "https://user:pass@bridge.simplefin.org/simplefin"

    with patch("simplefin_app.simplefin.httpx.post", return_value=mock_response) as mock_post:
        access_url = claim_setup_token(setup_token)

    assert access_url == "https://user:pass@bridge.simplefin.org/simplefin"
    mock_post.assert_called_once_with(claim_url, timeout=10.0)


def test_claim_setup_token_invalid_base64():
    try:
        claim_setup_token("not-valid-base64!!!")
        assert False, "Expected SimpleFinError"
    except SimpleFinError:
        pass


def test_claim_setup_token_rejected():
    claim_url = "https://bridge.simplefin.org/claim/abc123"
    setup_token = base64.b64encode(claim_url.encode()).decode()

    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"

    with patch("simplefin_app.simplefin.httpx.post", return_value=mock_response):
        try:
            claim_setup_token(setup_token)
            assert False, "Expected SimpleFinError"
        except SimpleFinError as e:
            assert "403" in str(e)


def test_claim_setup_token_network_error():
    import httpx

    claim_url = "https://bridge.simplefin.org/claim/abc123"
    setup_token = base64.b64encode(claim_url.encode()).decode()

    with patch(
        "simplefin_app.simplefin.httpx.post",
        side_effect=httpx.RequestError("connection refused"),
    ):
        try:
            claim_setup_token(setup_token)
            assert False, "Expected SimpleFinError"
        except SimpleFinError as e:
            assert "Network error" in str(e)
