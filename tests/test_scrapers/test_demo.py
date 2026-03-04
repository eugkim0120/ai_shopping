"""Tests for the demo data scraper."""

import pytest

from ai_shopping.scrapers.demo import DemoScraper


@pytest.fixture
def amazon_demo():
    return DemoScraper("amazon")


@pytest.fixture
def ebay_demo():
    return DemoScraper("ebay")


@pytest.mark.asyncio
async def test_search_returns_matching_items(amazon_demo):
    results = await amazon_demo.search("headphones")
    assert len(results) > 0
    assert all("headphone" in r.title.lower() or "airpod" in r.title.lower() for r in results)


@pytest.mark.asyncio
async def test_search_respects_max_price(amazon_demo):
    results = await amazon_demo.search("headphones", max_price="100")
    for r in results:
        assert r.price is not None
        price_val = float(r.price.replace("£", "").replace(",", ""))
        assert price_val <= 100.0


@pytest.mark.asyncio
async def test_search_returns_empty_for_no_match(amazon_demo):
    results = await amazon_demo.search("xyznonexistent12345")
    assert len(results) == 0


@pytest.mark.asyncio
async def test_items_have_correct_marketplace(amazon_demo):
    results = await amazon_demo.search("monitor")
    for r in results:
        assert r.marketplace == "amazon"


@pytest.mark.asyncio
async def test_items_have_raw_attributes(amazon_demo):
    results = await amazon_demo.search("monitor")
    assert len(results) > 0
    assert len(results[0].raw_attributes) > 0


@pytest.mark.asyncio
async def test_ebay_has_different_items(ebay_demo):
    results = await ebay_demo.search("headphones")
    assert len(results) > 0
    assert results[0].marketplace == "ebay"


@pytest.mark.asyncio
async def test_colour_filter(amazon_demo):
    results = await amazon_demo.search("jacket black", colour="black")
    # Should still return results that match the query
    assert isinstance(results, list)
