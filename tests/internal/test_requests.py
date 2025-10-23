import pytest
import requests
import time

API_ENDPOINT = "https://miniurl.gr/api/v1.0/minify"

def minify_url(session, url):
    payload = {"url": url}
    start_time = time.time()
    response = session.post(API_ENDPOINT, json=payload)
    elapsed = time.time() - start_time

    if response.status_code == 200:
        minified = response.json().get("minified_url", "")
        return minified, elapsed, response.status_code
    else:
        return None, elapsed, response.status_code

def test_minify_url_success():
    url = "https://www.example.com"
    with requests.Session() as session:
        minified, elapsed, status = minify_url(session, url)

    assert status == 200
    assert minified is not None
    assert minified.startswith("https://miniurl.gr/")
    assert elapsed >= 0

@pytest.mark.parametrize("url", [
    "http://tsaklidis.gr",
    "https://www.google.com",
    "https://github.com",
    "https://www.python.org"
])
def test_minify_url_various(url):
    with requests.Session() as session:
        minified, elapsed, status = minify_url(session, url)

    assert status == 200
    assert minified is not None
    assert minified.startswith("https://miniurl.gr/")
    assert elapsed >= 0

def test_minify_url_invalid():
    url = "not_a_url"
    with requests.Session() as session:
        minified, elapsed, status = minify_url(session, url)

    # The service might return 400 Bad Request or similar
    assert status != 200
    assert minified is None or minified == ""
    assert elapsed >= 0