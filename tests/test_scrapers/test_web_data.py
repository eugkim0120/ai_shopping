"""Tests for the web-sourced data scraper."""

import pytest

from ai_shopping.scrapers.web_data import WebDataScraper


@pytest.fixture
def amazon_web():
    return WebDataScraper("amazon")


@pytest.fixture
def ebay_web():
    return WebDataScraper("ebay")


@pytest.mark.asyncio
async def test_search_returns_real_products(amazon_web):
    results = await amazon_web.search("bluetooth speaker")
    assert len(results) > 0
    # At least most results should be speakers
    speaker_count = sum(1 for r in results if "speaker" in r.title.lower() or "bluetooth" in r.title.lower())
    assert speaker_count >= len(results) * 0.5


@pytest.mark.asyncio
async def test_search_returns_real_urls(amazon_web):
    results = await amazon_web.search("bluetooth speaker")
    assert len(results) > 0
    for r in results:
        assert "amazon.co.uk" in r.url


@pytest.mark.asyncio
async def test_search_respects_max_price(amazon_web):
    results = await amazon_web.search("speaker", max_price="100")
    for r in results:
        assert r.price is not None
        price_val = float(r.price.replace("£", "").replace(",", ""))
        assert price_val <= 100.0


@pytest.mark.asyncio
async def test_search_returns_empty_for_no_match(amazon_web):
    results = await amazon_web.search("xyznonexistent12345")
    assert len(results) == 0


@pytest.mark.asyncio
async def test_items_have_correct_marketplace(amazon_web):
    results = await amazon_web.search("keyboard")
    for r in results:
        assert r.marketplace == "amazon"


@pytest.mark.asyncio
async def test_items_have_raw_attributes(amazon_web):
    results = await amazon_web.search("keyboard")
    assert len(results) > 0
    assert len(results[0].raw_attributes) > 0


@pytest.mark.asyncio
async def test_ebay_has_different_items(ebay_web):
    results = await ebay_web.search("headphones")
    assert len(results) > 0
    assert results[0].marketplace == "ebay"


@pytest.mark.asyncio
async def test_multiple_categories_searchable(amazon_web):
    """Verify that diverse product categories return results."""
    queries = ["robot vacuum", "hiking boots", "power bank", "espresso machine", "tablet"]
    for q in queries:
        results = await amazon_web.search(q)
        assert len(results) > 0, f"No results for '{q}'"


@pytest.mark.asyncio
async def test_condition_filter(ebay_web):
    results = await ebay_web.search("headphones", condition="refurbished")
    assert isinstance(results, list)
