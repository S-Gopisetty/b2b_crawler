from dataclasses import dataclass
from pathlib import Path


@dataclass
class CrawlerConfig:
    category_url: str
    max_products: int = 10
    request_timeout: int = 15
    max_retries: int = 3
    retry_delay_sec: float = 2.0
    output_dir: Path = Path("output")


CONFIG = CrawlerConfig(
    category_url="https://dir.indiamart.com/impcat/paper-cup-making-machine.html",
    max_products=10,
)
