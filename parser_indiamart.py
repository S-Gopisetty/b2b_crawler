import re
from datetime import datetime
from typing import List, Dict, Optional

from bs4 import BeautifulSoup

from parser_base import ProductRecord


def _parse_price_value(price_text: Optional[str]) -> Optional[float]:
    """Extract numeric price from '₹ 7,50,000' -> 750000.0"""
    if not price_text:
        return None
    digits = re.sub(r"[^\d.]", "", price_text)
    if not digits:
        return None
    try:
        return float(digits)
    except ValueError:
        return None


class IndiaMartParser:
    marketplace = "indiamart"

    def extract_product_links(self, html: str) -> List[str]:
        soup = BeautifulSoup(html, "lxml")
        links: List[str] = []
        for a in soup.select("a.prdtitle"):
            href = a.get("href")
            if href and "proddetail" in href:
                links.append(href.strip())
        if not links:
            for a in soup.select("a[href*='proddetail']"):
                href = a.get("href")
                if href:
                    links.append(href.strip())
        seen = set()
        uniq: List[str] = []
        for url in links:
            if url not in seen:
                seen.add(url)
                uniq.append(url)

        print(f"[INFO] Found {len(uniq)} unique product links on listing page")
        return uniq

    def parse_product_page(self, html: str, url: str) -> ProductRecord:
        soup = BeautifulSoup(html, "lxml")
        name_el = soup.select_one("h1.center-heading")
        product_name = name_el.get_text(strip=True) if name_el else None
        price_el = soup.select_one(".price-unit")
        price_text = price_el.get_text(strip=True) if price_el else None
        price_value = _parse_price_value(price_text)

        currency: Optional[str] = None
        if price_text:
            if "₹" in price_text or "Rs" in price_text:
                currency = "INR"
            elif "$" in price_text:
                currency = "USD"
        city_el = soup.select_one(".city-highlight")
        location_city = city_el.get_text(strip=True) if city_el else None
        location_full: Optional[str] = None
        company_box = soup.select_one(".company-box")
        if company_box:
            for span in company_box.select("span"):
                text = span.get_text(" ", strip=True)
                if "India" in text and any(ch.isdigit() for ch in text):
                    location_full = text
                    break
        specs: Dict[str, str] = {}
        table = soup.select_one(".isq-container table")
        if table:
            for tr in table.select("tr"):
                cells = [td.get_text(" ", strip=True) for td in tr.select("td")]
                if len(cells) >= 2 and cells[0] and cells[1]:
                    specs[cells[0]] = cells[1]
        desc_el = soup.select_one("#descp2 .pro-descN")
        description = desc_el.get_text(" ", strip=True) if desc_el else None
        company_name: Optional[str] = None
        if company_box:
            h2 = company_box.select_one("h2")
            if h2:
                company_name = h2.get_text(strip=True)

        cp_el = soup.select_one("#supp_nm")
        contact_person = cp_el.get_text(strip=True) if cp_el else None

        company_website: Optional[str] = None
        if company_box:
            web_el = company_box.select_one("a[href^='http']")
            if web_el:
                company_website = web_el.get("href")

        gst: Optional[str] = None
        if company_box:
            spans = list(company_box.select("span"))
            for i, sp in enumerate(spans):
                if sp.get_text(strip=True).upper() == "GST":
                    j = i + 1
                    while j < len(spans):
                        candidate = spans[j].get_text(strip=True)
                        if candidate and candidate != "-":
                            gst = candidate
                            break
                        j += 1
                    break

        scraped_at = datetime.utcnow().isoformat() + "Z"

        return ProductRecord(
            marketplace=self.marketplace,
            product_name=product_name,
            product_url=url,
            price_text=price_text,
            price_value=price_value,
            currency=currency,
            location_city=location_city,
            location_full=location_full,
            specs=specs,
            description=description,
            company_name=company_name,
            contact_person=contact_person,
            company_website=company_website,
            gst=gst,
            scraped_at=scraped_at,
        )
