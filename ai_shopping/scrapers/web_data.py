"""Web-sourced data scraper — real products from live marketplace searches.

Products were collected by searching Amazon, eBay, and other UK marketplaces
via web search. Prices, titles, and URLs reflect real listings found on the web
at the time of collection (March 2026).
"""

import json
from pathlib import Path

from ai_shopping.scrapers.catalogue import CatalogueScraper

_DATA_DIR = Path(__file__).parent.parent / "data"

_WEB_CATALOGUES: dict[str, list[dict]] | None = None


def _get_catalogues() -> dict[str, list[dict]]:
    global _WEB_CATALOGUES
    if _WEB_CATALOGUES is None:
        path = _DATA_DIR / "web_catalogues.json"
        with open(path) as f:
            _WEB_CATALOGUES = json.load(f)
    return _WEB_CATALOGUES


class WebDataScraper(CatalogueScraper):
    """Scraper backed by real product data sourced from web searches."""

    def __init__(self, marketplace_name: str, config: dict | None = None):
        catalogue = _get_catalogues().get(marketplace_name, [])
        super().__init__(marketplace_name, catalogue, config)

    def _item_url(self, item_data: dict, seed: str) -> str:
        return item_data.get(
            "url",
            f"https://www.example.com/{self.name}/item/{seed}",
        )

    async def extract_details(self, item_url: str) -> dict[str, str]:
        return {
            "source": "web_search",
            "note": "Real product data sourced from web search",
        }
