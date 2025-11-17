from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class ProductRecord:
    marketplace: str
    product_name: Optional[str]
    product_url: str
    price_text: Optional[str]
    price_value: Optional[float]
    currency: Optional[str]
    location_city: Optional[str]
    location_full: Optional[str]
    specs: Dict[str, str]
    description: Optional[str]
    company_name: Optional[str]
    contact_person: Optional[str]
    company_website: Optional[str]
    gst: Optional[str]
    scraped_at: str
