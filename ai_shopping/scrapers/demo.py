"""Demo data provider — realistic mock results for development and testing."""

import json
from pathlib import Path

from ai_shopping.scrapers.catalogue import CatalogueScraper

_DATA_DIR = Path(__file__).parent.parent / "data"

_CATALOGUES: dict[str, list[dict]] | None = None


def _get_catalogues() -> dict[str, list[dict]]:
    global _CATALOGUES
    if _CATALOGUES is None:
        path = _DATA_DIR / "demo_catalogues.json"
        with open(path) as f:
            _CATALOGUES = json.load(f)
    return _CATALOGUES


class DemoScraper(CatalogueScraper):
    """Mock data scraper — used when real scrapers are unavailable."""

    def __init__(self, marketplace_name: str, config: dict | None = None):
        catalogue = _get_catalogues().get(marketplace_name, [])
        super().__init__(marketplace_name, catalogue, config)

    async def extract_details(self, item_url: str) -> dict[str, str]:
        return {"source": "demo", "note": "This is demo data"}
