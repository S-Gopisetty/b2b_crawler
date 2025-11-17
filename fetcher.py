import time
from typing import Optional

import requests

from config import CONFIG


class HttpFetcher:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-IN,en;q=0.9",
                "Connection": "keep-alive",
                "Referer": "https://www.indiamart.com/",
            }
        )

    def fetch_html(self, url: str) -> Optional[str]:
        """
        Fetch raw HTML from URL with a few retries and basic backoff.
        Returns HTML as string or None on failure.
        """
        for attempt in range(1, CONFIG.max_retries + 1):
            try:
                print(f"[INFO] Fetching ({attempt}/{CONFIG.max_retries}) {url}")
                resp = self.session.get(url, timeout=CONFIG.request_timeout)
                print(f"[INFO] Status code: {resp.status_code}")

                if resp.status_code == 200:
                    return resp.text

                if resp.status_code in (429, 403, 503):
                    print(f"[WARN] Server responded {resp.status_code}, backing off...")
                    time.sleep(CONFIG.retry_delay_sec * attempt)
                    continue

                print(f"[ERROR] Non-OK status {resp.status_code} for {url}")
                return None

            except requests.RequestException as exc:
                print(f"[ERROR] Request failed for {url}: {exc}")
                time.sleep(CONFIG.retry_delay_sec * attempt)

        print(f"[ERROR] Failed to fetch {url} after {CONFIG.max_retries} retries")
        return
