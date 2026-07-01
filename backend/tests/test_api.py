import base64
from unittest.mock import patch, MagicMock

import pytest
from ninja.testing import TestClient

from config.api import api

client = TestClient(api)


@pytest.mark.django_db
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_status_not_connected():
    response = client.get("/simplefin/status")
    assert response.status_code == 200
    assert response.json() == {"connected": False}


@pytest.mark.django_db
def test_connect_and_status():
    claim_url = "https://bridge.simplefin.org/claim/abc123"
    setup_token = base64.b64encode(claim_url.encode()).decode()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "https://user:pass@bridge.simplefin.org/simplefin"

    with patch("simplefin_app.simplefin.httpx.post", return_value=mock_response):
        response = client.post(
            "/simplefin/connect", json={"setup_token": setup_token}
        )

    assert response.status_code == 200
    assert response.json() == {"status": "connected"}

    # Status should now reflect the connection
    status = client.get("/simplefin/status")
    assert status.json() == {"connected": True}


@pytest.mark.django_db
def test_accounts_no_connection():
    response = client.get("/accounts/")
    assert response.status_code == 400
