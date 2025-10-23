import pytest
import requests
import time
import os
from faker import Faker

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MINIFY_ENDPOINT = f"{BASE_URL}/api/v1.0/minify"

fake = Faker()

def wait_for_api(url, timeout=30):
    """Wait until the API is up (simple health check on root endpoint or minify)."""
    for _ in range(timeout):
        try:
            # Try root and minify endpoints
            resp_root = requests.get(url)
            resp_minify = requests.post(MINIFY_ENDPOINT, json={"url": "http://example.com/?from_tests=True"})
            if resp_root.status_code in [200, 404] or resp_minify.status_code in [200, 201, 404]:
                return True
        except Exception:
            time.sleep(1)
    return False

@pytest.fixture(scope="session", autouse=True)
def ensure_api():
    assert wait_for_api(BASE_URL), f"API not available at {BASE_URL}"

@pytest.fixture
def random_url():
    base = fake.url()
    param_key = fake.word()
    param_val = fake.word()
    return f"{base}?{param_key}={param_val}&id={fake.random_int()}&from_tests=True"

def test_minify_status_code(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"

def test_minified_url_in_response(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"
    data = response.json()
    assert "minified_url" in data, f"Missing minified_url in response: {data}"

def test_redirect_is_301(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"
    minified_url = response.json().get("minified_url")
    assert minified_url, "No minified_url in response"
    redirect_response = requests.get(minified_url, allow_redirects=False)
    assert redirect_response.status_code in [301, 302], f"Unexpected redirect status: {redirect_response.status_code}"

def test_alias_returns_original_url(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"
    minified_url = response.json().get("minified_url")
    assert minified_url, "No minified_url in response"
    alias = minified_url.rstrip('/').split('/')[-1]
    api_alias_endpoint = f"{BASE_URL}/api/v1.0/{alias}"

    # Retry logic in case alias is not immediately available
    for _ in range(3):
        alias_response = requests.get(api_alias_endpoint)
        if alias_response.status_code == 200:
            break
        time.sleep(0.5)
    assert alias_response.status_code == 200, f"Alias endpoint returned {alias_response.status_code}"
    alias_data = alias_response.json()
    assert "url" in alias_data, f"Missing url in alias_data: {alias_data}"
    assert alias_data["url"] == random_url

def test_response_times_under_1500ms(random_url):
    start = time.time()
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 1500, f"Minify POST took too long: {elapsed_ms}ms"
    assert response.status_code in [200, 201], f"Unexpected status code: {response.status_code}"

    minified_url = response.json().get("minified_url")
    assert minified_url, "No minified_url in response"
    start = time.time()
    redirect_response = requests.get(minified_url, allow_redirects=False)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 1500, f"Redirect GET took too long: {elapsed_ms}ms"
    assert redirect_response.status_code in [301, 302], f"Unexpected redirect status: {redirect_response.status_code}"

    alias = minified_url.rstrip('/').split('/')[-1]
    api_alias_endpoint = f"{BASE_URL}/api/v1.0/{alias}"
    start = time.time()
    alias_response = requests.get(api_alias_endpoint)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 1500, f"Alias GET took too long: {elapsed_ms}ms"
    assert alias_response.status_code == 200, f"Alias endpoint returned {alias_response.status_code}"