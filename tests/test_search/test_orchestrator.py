"""Integration tests for the search orchestrator."""

import pytest

from ai_shopping.categorisation.engine import CategorisationEngine
from ai_shopping.scrapers.registry import ScraperRegistry
from ai_shopping.scrapers.web_data import WebDataScraper
from ai_shopping.search.detector import SearchDetector
from ai_shopping.search.orchestrator import SearchOrchestrator


@pytest.fixture
def orchestrator():
    registry = ScraperRegistry()
    for name in ["amazon", "ebay", "gumtree", "facebook_marketplace", "vinted"]:
        registry.register(WebDataScraper(name))
    detector = SearchDetector()
    categoriser = CategorisationEngine()
    return SearchOrchestrator(
        registry, detector, categoriser, use_demo_fallback=True,
    )


@pytest.mark.asyncio
async def test_search_returns_items(orchestrator):
    result = await orchestrator.search("bluetooth speaker")
    assert result["total"] > 0
    assert len(result["items"]) > 0


@pytest.mark.asyncio
async def test_search_returns_filter_options(orchestrator):
    result = await orchestrator.search("bluetooth speaker")
    assert "brand" in result["filter_options"]
    assert "marketplace" in result["filter_options"]


@pytest.mark.asyncio
async def test_search_respects_brand_filter(orchestrator):
    result = await orchestrator.search("headphones Sony")
    for item in result["items"]:
        brand = item.raw_attributes.get("brand", "").lower()
        title = item.title.lower()
        assert "sony" in brand or "sony" in title


@pytest.mark.asyncio
async def test_search_respects_price_filter(orchestrator):
    result = await orchestrator.search("speaker under £100")
    for item in result["items"]:
        price = item.price.replace("£", "").replace(",", "")
        assert float(price) <= 100.0


@pytest.mark.asyncio
async def test_search_respects_marketplace_filter(orchestrator):
    result = await orchestrator.search("speaker on amazon")
    for item in result["items"]:
        assert item.marketplace == "amazon"


@pytest.mark.asyncio
async def test_empty_query_returns_empty(orchestrator):
    result = await orchestrator.search("")
    assert result["total"] == 0


@pytest.mark.asyncio
async def test_search_returns_intent(orchestrator):
    result = await orchestrator.search("black Sony headphones under £300")
    intent = result["intent"]
    assert intent.colour == "black"
    assert intent.brand == "sony"
    assert intent.max_price == 300.0
