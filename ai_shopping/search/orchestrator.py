"""Search orchestrator — runs searches across multiple marketplaces concurrently."""

import asyncio

from ai_shopping.categorisation.engine import CategorisationEngine
from ai_shopping.scrapers.base import ScrapedItem
from ai_shopping.scrapers.registry import ScraperRegistry
from ai_shopping.search.detector import SearchDetector, SearchIntent


class SearchOrchestrator:
    """Coordinates searches across all registered scrapers and applies categorisation."""

    def __init__(
        self,
        registry: ScraperRegistry,
        detector: SearchDetector,
        categoriser: CategorisationEngine,
    ):
        self.registry = registry
        self.detector = detector
        self.categoriser = categoriser

    async def search(self, raw_query: str) -> dict:
        intent = self.detector.parse(raw_query)
        scrapers = self._select_scrapers(intent)

        filters = {}
        if intent.min_price is not None:
            filters["min_price"] = str(intent.min_price)
        if intent.max_price is not None:
            filters["max_price"] = str(intent.max_price)

        tasks = [scraper.search(intent.query, **filters) for scraper in scrapers]
        results_lists = await asyncio.gather(*tasks, return_exceptions=True)

        all_items: list[ScrapedItem] = []
        errors: list[str] = []
        for i, result in enumerate(results_lists):
            if isinstance(result, Exception):
                errors.append(f"{scrapers[i].name}: {result}")
            else:
                all_items.extend(result)

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
