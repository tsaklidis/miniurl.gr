import pytest
import requests
import time
import os
from faker import Faker

from app.core.config import settings

BASE_URL = "https://miniurl.gr"
MINIFY_ENDPOINT = f"{BASE_URL}/api/v1.0/minify"

fake = Faker()

@pytest.fixture
def random_url():
    base = fake.url()
    param_key = fake.word()
    param_val = fake.word()
    return f"{base}?{param_key}={param_val}&id={fake.random_int()}&from_tests=True"

def test_minify_status_code(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    assert response.status_code == 200

def test_minified_url_in_response(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    data = response.json()
    assert "minified_url" in data

def test_redirect_is_301(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    minified_url = response.json()["minified_url"]
    redirect_response = requests.get(minified_url, allow_redirects=False)
    assert redirect_response.status_code == 301

def test_alias_returns_original_url(random_url):
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    minified_url = response.json()["minified_url"]
    alias = minified_url.split('/')[-1]
    api_alias_endpoint = f"{BASE_URL}/api/v1.0/{alias}"
    alias_response = requests.get(api_alias_endpoint)
    alias_data = alias_response.json()
    assert "url" in alias_data
    assert alias_data["url"] == random_url

def test_response_times_under_1000ms(random_url):
    start = time.time()
    response = requests.post(MINIFY_ENDPOINT, json={"url": random_url})
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 1000

    minified_url = response.json()["minified_url"]
    start = time.time()
    redirect_response = requests.get(minified_url, allow_redirects=False)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 1000

    alias = minified_url.split('/')[-1]
    api_alias_endpoint = f"{BASE_URL}/api/v1.0/{alias}"
    start = time.time()
    alias_response = requests.get(api_alias_endpoint)
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 1000