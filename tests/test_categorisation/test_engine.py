"""Tests for the auto-categorisation engine."""

from ai_shopping.categorisation.engine import CategorisationEngine
from ai_shopping.scrapers.base import ScrapedItem


def make_item(title="Test Item", price=None, attrs=None):
    return ScrapedItem(
        title=title,
        price=price,
        marketplace="test",
        raw_attributes=attrs or {},
    )


def test_extracts_price_category():
    engine = CategorisationEngine()
    items = [make_item(price="£199.99"), make_item(price="£299.00")]
    categories = engine.analyse_items(items)
    assert "price" in categories
    assert len(categories["price"].values) == 2


def test_extracts_colour_from_title():
    engine = CategorisationEngine()
    items = [
        make_item(title="Black iPhone 15"),
        make_item(title="White Samsung Galaxy"),
        make_item(title="Black Pixel 8"),
    ]
    categories = engine.analyse_items(items)
    assert "colour" in categories
    assert "Black" in categories["colour"].values
    assert "White" in categories["colour"].values


def test_extracts_size_spec_from_title():
    engine = CategorisationEngine()
    items = [
        make_item(title="MacBook Pro 512GB"),
        make_item(title="iPad 256GB"),
    ]
    categories = engine.analyse_items(items)
    assert "size_or_spec" in categories


def test_extracts_brand_from_attributes():
    engine = CategorisationEngine()
    items = [
        make_item(attrs={"Brand": "Apple"}),
        make_item(attrs={"Brand": "Samsung"}),
        make_item(attrs={"Brand": "Apple"}),
    ]
    categories = engine.analyse_items(items)
    assert "brand" in categories
    assert "Apple" in categories["brand"].values
    assert "Samsung" in categories["brand"].values


def test_get_filter_options_returns_sorted_values():
    engine = CategorisationEngine()
    items = [
        make_item(title="Blue Shirt", price="£20"),
        make_item(title="Red Shirt", price="£25"),
        make_item(title="Blue Trousers", price="£30"),
    ]
    options = engine.get_filter_options(items)
    assert "colour" in options
    assert options["colour"] == ["Blue", "Red"]


def test_empty_items_returns_empty_categories():
    engine = CategorisationEngine()
    categories = engine.analyse_items([])
    assert categories == {}
