"""Marketplace scrapers package."""

from ai_shopping.scrapers.base import BaseScraper
from ai_shopping.scrapers.registry import ScraperRegistry

__all__ = ["BaseScraper", "ScraperRegistry"]
