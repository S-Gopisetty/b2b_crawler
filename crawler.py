from typing import List

from config import CONFIG
from fetcher import HttpFetcher
from parser_indiamart import IndiaMartParser
from parser_base import ProductRecord


class IndiaMartCategoryCrawler:

    def __init__(self) -> None:
        self.fetcher = HttpFetcher()
        self.parser = IndiaMartParser()

    def crawl(self) -> List[ProductRecord]:
        print(f"[INFO] Fetching listing page: {CONFIG.category_url}")
        listing_html = self.fetcher.fetch_html(CONFIG.category_url)
        if listing_html is None:
            print("[ERROR] Could not fetch listing page.")
            return []

        product_urls = self.parser.extract_product_links(listing_html)
        if not product_urls:
            print("[WARN] No product URLs found on listing page.")
            return []

        if CONFIG.max_products:
            product_urls = product_urls[: CONFIG.max_products]

        print(f"[INFO] Crawling {len(product_urls)} product pages...\n")

        records: List[ProductRecord] = []

        for idx, url in enumerate(product_urls, start=1):
            print(f"[INFO] [{idx}/{len(product_urls)}] Fetch product: {url}")
            html = self.fetcher.fetch_html(url)
            if html is None:
                print(f"[WARN] Skipping (fetch failed): {url}")
                continue

            try:
                record = self.parser.parse_product_page(html, url)
                records.append(record)
            except Exception as exc:
                print(f"[ERROR] Failed to parse {url}: {exc}")

        print(f"\n[INFO] Finished. Parsed {len(records)} products.")
        return records
