"""Tests for the scraper registry."""

import pytest

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem
from ai_shopping.scrapers.registry import ScraperRegistry


class FakeScraper(BaseScraper):
    name = "fake"

    async def search(self, query, **filters):
        return [ScrapedItem(title=f"Fake: {query}", marketplace=self.name)]

    async def extract_details(self, item_url):
        return {"source": "fake"}


class AnotherFakeScraper(BaseScraper):
    name = "another"

    async def search(self, query, **filters):
        return []

    async def extract_details(self, item_url):
        return {}


def test_register_and_get():
    registry = ScraperRegistry()
    scraper = FakeScraper()
    registry.register(scraper)
    assert registry.get("fake") is scraper


def test_get_returns_none_for_unknown():
    registry = ScraperRegistry()
    assert registry.get("nonexistent") is None


def test_all_returns_registered_scrapers():
    registry = ScraperRegistry()
    s1 = FakeScraper()
    s2 = AnotherFakeScraper()
    registry.register(s1)
    registry.register(s2)
    assert set(registry.names()) == {"fake", "another"}
    assert len(registry.all()) == 2


@pytest.mark.asyncio
async def test_fake_scraper_search():
    scraper = FakeScraper()
    results = await scraper.search("laptop")
    assert len(results) == 1
    assert results[0].title == "Fake: laptop"
    assert results[0].marketplace == "fake"
