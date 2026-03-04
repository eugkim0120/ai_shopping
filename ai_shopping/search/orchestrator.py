"""Search orchestrator — runs searches across multiple marketplaces concurrently."""

import asyncio
import logging

from ai_shopping.categorisation.engine import CategorisationEngine
from ai_shopping.scrapers.base import ScrapedItem
from ai_shopping.scrapers.web_data import WebDataScraper
from ai_shopping.scrapers.registry import ScraperRegistry
from ai_shopping.search.detector import SearchDetector, SearchIntent

logger = logging.getLogger(__name__)


class SearchOrchestrator:
    """Coordinates searches across all registered scrapers and applies categorisation."""

    def __init__(
        self,
        registry: ScraperRegistry,
        detector: SearchDetector,
        categoriser: CategorisationEngine,
        use_demo_fallback: bool = True,
    ):
        self.registry = registry
        self.detector = detector
        self.categoriser = categoriser
        self.use_demo_fallback = use_demo_fallback
        self._demo_scrapers: dict[str, WebDataScraper] = {}

    def _get_demo_scraper(self, marketplace_name: str) -> WebDataScraper:
        if marketplace_name not in self._demo_scrapers:
            self._demo_scrapers[marketplace_name] = WebDataScraper(marketplace_name)
        return self._demo_scrapers[marketplace_name]

    async def search(self, raw_query: str) -> dict:
        intent = self.detector.parse(raw_query)
        scrapers = self._select_scrapers(intent)

        filters = {}
        if intent.min_price is not None:
            filters["min_price"] = str(intent.min_price)
        if intent.max_price is not None:
            filters["max_price"] = str(intent.max_price)
        if intent.colour:
            filters["colour"] = intent.colour
        if intent.condition:
            filters["condition"] = intent.condition
        if intent.brand:
            filters["brand"] = intent.brand

        tasks = [scraper.search(intent.query, **filters) for scraper in scrapers]
        results_lists = await asyncio.gather(*tasks, return_exceptions=True)

        all_items: list[ScrapedItem] = []
        errors: list[str] = []
        failed_scrapers: list[str] = []

        for i, result in enumerate(results_lists):
            if isinstance(result, Exception):
                scraper_name = scrapers[i].name
                errors.append(f"{scraper_name}: {result}")
                failed_scrapers.append(scraper_name)
                logger.warning("Scraper %s failed: %s", scraper_name, result)
            else:
                all_items.extend(result)

        # Demo fallback for scrapers that failed
        if self.use_demo_fallback and failed_scrapers:
            demo_tasks = []
            demo_names = []
            for name in failed_scrapers:
                demo = self._get_demo_scraper(name)
                demo_tasks.append(demo.search(intent.query, **filters))
                demo_names.append(name)

            demo_results = await asyncio.gather(*demo_tasks, return_exceptions=True)
            demo_count = 0
            for j, demo_result in enumerate(demo_results):
                if isinstance(demo_result, Exception):
                    logger.warning("Demo scraper %s also failed: %s", demo_names[j], demo_result)
                else:
                    all_items.extend(demo_result)
                    demo_count += len(demo_result)

            if demo_count > 0:
                errors = [f"Showing web-sourced results ({demo_count} items) — live scraping unavailable"]

        # Keep relevance order from scrapers (they return items sorted by score)

        filter_options = self.categoriser.get_filter_options(all_items)

        return {
            "intent": intent,
            "items": all_items,
            "filter_options": filter_options,
            "total": len(all_items),
            "errors": errors,
        }

    def _select_scrapers(self, intent: SearchIntent):
        if intent.marketplaces:
            selected = []
            for name in intent.marketplaces:
                scraper = self.registry.get(name)
                if scraper:
                    selected.append(scraper)
            return selected if selected else self.registry.all()
        return self.registry.all()


def _parse_price(price_str: str) -> float:
    try:
        cleaned = price_str.replace("£", "").replace("$", "").replace("€", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return float("inf")
