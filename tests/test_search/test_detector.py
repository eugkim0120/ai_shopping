"""Tests for search intent detection."""

from ai_shopping.search.detector import SearchDetector


def test_basic_query():
    detector = SearchDetector()
    intent = detector.parse("laptop")
    assert "laptop" in intent.query


def test_extracts_max_price():
    detector = SearchDetector()
    intent = detector.parse("iPhone under £500")
    assert intent.max_price == 500.0


def test_extracts_min_price():
    detector = SearchDetector()
    intent = detector.parse("laptop over £1000")
    assert intent.min_price == 1000.0


def test_extracts_price_range():
    detector = SearchDetector()
    intent = detector.parse("tablet £200 - £500")
    assert intent.min_price == 200.0
    assert intent.max_price == 500.0


def test_extracts_colour():
    detector = SearchDetector()
    intent = detector.parse("black iPhone")
    assert intent.colour == "black"


def test_extracts_condition():
    detector = SearchDetector()
    intent = detector.parse("used MacBook")
    assert intent.condition == "used"


def test_extracts_marketplace():
    detector = SearchDetector()
    intent = detector.parse("trainers on ebay")
    assert "ebay" in intent.marketplaces


def test_extracts_facebook_alias():
    detector = SearchDetector()
    intent = detector.parse("sofa on facebook")
    assert "facebook_marketplace" in intent.marketplaces


def test_complex_query():
    detector = SearchDetector()
    intent = detector.parse("black Nike trainers under £100 on ebay")
    assert intent.max_price == 100.0
    assert intent.colour == "black"
    assert "ebay" in intent.marketplaces
    assert "nike" in intent.query.lower() or "trainers" in intent.query.lower()


def test_no_filters_detected():
    detector = SearchDetector()
    intent = detector.parse("wireless keyboard")
    assert intent.min_price is None
    assert intent.max_price is None
    assert intent.colour is None
    assert intent.condition is None
    assert intent.marketplaces == []


def test_extracts_brand():
    detector = SearchDetector()
    intent = detector.parse("Samsung phone")
    assert intent.brand == "samsung"


def test_extracts_material():
    detector = SearchDetector()
    intent = detector.parse("leather handbag")
    assert intent.material == "leather"


def test_extracts_size():
    detector = SearchDetector()
    intent = detector.parse("running shoes size 10")
    assert intent.size == "10"


def test_condition_like_new():
    detector = SearchDetector()
    intent = detector.parse("like new sofa")
    assert intent.condition == "like new"


def test_condition_refurbished():
    detector = SearchDetector()
    intent = detector.parse("refurbished Dyson vacuum")
    assert intent.condition == "refurbished"
    assert intent.brand == "dyson"
