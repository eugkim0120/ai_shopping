"""Tests for shared utilities."""

from ai_shopping.utils import parse_price


def test_parse_gbp():
    assert parse_price("£129.99") == 129.99


def test_parse_with_comma():
    assert parse_price("£1,199.00") == 1199.00


def test_parse_usd():
    assert parse_price("$49.99") == 49.99


def test_parse_euro():
    assert parse_price("€25.00") == 25.00


def test_parse_none_returns_none():
    assert parse_price(None) is None


def test_parse_empty_returns_none():
    assert parse_price("") is None


def test_parse_garbage_returns_none():
    assert parse_price("not a price") is None
