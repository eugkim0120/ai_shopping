"""Scraper registry — discovers and manages marketplace scrapers."""

from ai_shopping.scrapers.base import BaseScraper


class ScraperRegistry:
    """Central registry for all available marketplace scrapers."""

    def __init__(self):
        self._scrapers: dict[str, BaseScraper] = {}

    def register(self, scraper: BaseScraper) -> None:
        self._scrapers[scraper.name] = scraper

    def get(self, name: str) -> BaseScraper | None:
        return self._scrapers.get(name)

    def all(self) -> list[BaseScraper]:
        return list(self._scrapers.values())

    def names(self) -> list[str]:
        return list(self._scrapers.keys())

    async def close_all(self):
        for scraper in self._scrapers.values():
            await scraper.close()
