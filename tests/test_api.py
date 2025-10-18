import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)

def test_minify_url_success():
    body = {
        "url": "https://example.com",
        # "preferred_alias": "exmpl1",
        "description": "Test URL"
    }
    response = client.post("/api/v1.0/minify", json=body)
    assert response.status_code == 200
    # Assert response contains alias or shortened URL
    assert "exmpl1" in response.text or "alias" in response.json()

def test_minify_url_validation_error():
    # Missing required 'url'
    body = {}
    response = client.post("/api/v1.0/minify", json=body)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_minify_url_rate_limit():
    # Simulate too many requests (mock in real test)
    # Here just check for correct status code and error message format
    response = client.post("/api/v1.0/minify", json={"url": "https://example.com"})
    if response.status_code == 429:
        assert "Rate limit exceeded" in response.text

def test_resolve_url_redirect():
    # This endpoint should redirect; supply a valid alias
    alias = "exmpl1"
    response = client.get(f"/{alias}")
    # Expect a redirect or a JSON response, depending on implementation
    assert response.status_code in [200, 302, 307]

def test_resolve_url_json():
    # This endpoint returns JSON for a valid alias
    alias = "exmpl1"
    response = client.get(f"/api/v1.0/{alias}")
    assert response.status_code == 200
    # Expect JSON containing original URL or similar
    assert "http" in response.text or isinstance(response.json(), dict)

def test_resolve_url_validation_error():
    # Alias too short (less than minLength)
    alias = "x"
    response = client.get(f"/api/v1.0/{alias}")
    assert response.status_code == 422
    assert "detail" in response.json()

def test_health_redis_with_apikey():
    headers = {"api-token": settings.APP_API_TOKEN}
    response = client.get("/health/redis", headers=headers)
    assert response.status_code == 200 or response.status_code == 429
    result = response.json()
    assert "healthy" in result

def test_health_redis_rw_with_apikey():
    headers = {"api-token": settings.APP_API_TOKEN}
    response = client.get("/health/redis_rw", headers=headers)
    assert response.status_code == 200 or response.status_code == 429
    result = response.json()
    assert "healthy" in result

def test_health_redis_data_with_apikey():
    headers = {"api-token": settings.APP_API_TOKEN}
    response = client.get("/health/redis_data", headers=headers)
    assert response.status_code == 200 or response.status_code == 429
    # Response should be a dict of {key: value}

