import os
import pytest
import httpx

BASE_URL = "https://miniurl.gr"
API_TOKEN = os.getenv("MINIURL_API_TOKEN")


# ----------------------
# 🟢 Public Endpoint Tests
# ----------------------

def test_health_psql_public():
    """
    /health/psql is public and should return 200 OK with {"message": True}.
    """
    url = f"{BASE_URL}/health/psql"
    response = httpx.get(url, timeout=10)
    assert response.status_code == 200, f"Unexpected status: {response.status_code}, body: {response.text}"
    data = response.json()
    assert data == {"message": True}, f"Unexpected response data: {data}"


# ----------------------
# 🔒 Protected Endpoints
# ----------------------

@pytest.mark.parametrize("endpoint", [
    "/health/redis",
    "/health/redis_rw",
    "/health/redis_data",
])
def test_protected_health_endpoints_authorized(endpoint):
    """
    Verify that all protected health endpoints return 200 OK when using a valid token.
    """
    if not API_TOKEN:
        pytest.skip("Environment variable MINIURL_API_TOKEN not set — skipping authorized tests.")

    url = f"{BASE_URL}{endpoint}"
    headers = {"api-token": API_TOKEN}

    response = httpx.get(url, headers=headers, timeout=10)
    assert response.status_code == 200, f"{endpoint} failed with {response.status_code}: {response.text}"

    data = response.json()
    assert isinstance(data, dict), f"{endpoint} did not return a JSON object: {data}"
    # Should contain at least one expected key
    assert any(k in data for k in ["healthy", "error", "message", "key1"]), f"Unexpected structure: {data}"


@pytest.mark.parametrize("endpoint", [
    "/health/redis",
    "/health/redis_rw",
    "/health/redis_data",
])
def test_protected_health_endpoints_no_auth(endpoint):
    """
    Requests without an API token should return 401 or 403.
    """
    url = f"{BASE_URL}{endpoint}"
    response = httpx.get(url, timeout=10)
    assert response.status_code in (401, 403), (
        f"{endpoint} should be unauthorized, got {response.status_code}: {response.text}"
    )


@pytest.mark.parametrize("endpoint", [
    "/health/redis",
    "/health/redis_rw",
    "/health/redis_data",
])
def test_protected_health_endpoints_invalid_token(endpoint):
    """
    Requests with an invalid API token should return 401 Unauthorized.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"api-token": "invalid-token"}

    response = httpx.get(url, headers=headers, timeout=10)
    assert response.status_code == 401, f"{endpoint} expected 401, got {response.status_code}: {response.text}"
    data = response.json()
    assert "Invalid credentials" in str(data), f"Unexpected response: {data}"
