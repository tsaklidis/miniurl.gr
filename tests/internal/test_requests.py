import requests
import time
from rich.console import Console
from rich.table import Table
from rich.progress import track

API_ENDPOINT = "https://miniurl.gr/api/v1.0/minify"

URLS = [
    "http://tsaklidis.gr",
    "https://www.google.com",
    "https://github.com",
    "https://www.python.org",
    "https://www.wikipedia.org",
    "https://www.bbc.com",
    "https://www.yahoo.com",
    "https://www.stackoverflow.com",
    "https://www.microsoft.com",
    "https://www.apple.com"
]

console = Console()

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

def main(urls):
    table = Table(title="URL Minification Stats", show_lines=True)
    table.add_column("Original URL", style="cyan", no_wrap=True)
    table.add_column("Minified URL", style="magenta")
    table.add_column("Time (s)", style="green")
    table.add_column("Status", style="yellow")

    # Use a requests.Session for performance
    with requests.Session() as session:
        for url in track(urls, description="Minifying URLs..."):
            minified, elapsed, status = minify_url(session, url)
            status_str = "✅ Success" if status == 200 else f"❌ Error ({status})"
            table.add_row(
                url,
                minified if minified else "-",
                f"{elapsed:.3f}",
                status_str
            )

    console.print(table)

if __name__ == "__main__":
    main(URLS)