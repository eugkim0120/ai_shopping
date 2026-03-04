"""Categorisation engine — discovers and extracts dynamic product categories."""

import re
from dataclasses import dataclass, field

from ai_shopping.scrapers.base import ScrapedItem


@dataclass
class Category:
    """A dynamically discovered category with its possible values."""

    name: str
    values: set[str] = field(default_factory=set)
    frequency: int = 0


PRICE_PATTERN = re.compile(r"[£$€]\s*[\d,]+\.?\d*")
COLOUR_WORDS = {
    "black", "white", "red", "blue", "green", "yellow", "orange", "purple",
    "pink", "grey", "gray", "brown", "silver", "gold", "navy", "beige",
}
SIZE_PATTERN = re.compile(r"\b(XS|S|M|L|XL|XXL|\d+\s*(?:GB|TB|MB|mm|cm|inch|\")|size\s*\d+)\b", re.I)
BRAND_INDICATORS = {"brand", "manufacturer", "make", "by"}


class CategorisationEngine:
    """Dynamically discovers categories from scraped items."""

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self._categories: dict[str, Category] = {}

    def analyse_items(self, items: list[ScrapedItem]) -> dict[str, Category]:
        self._categories.clear()

        for item in items:
            self._extract_from_title(item)
            self._extract_from_attributes(item)
            self._extract_price(item)

        return {k: v for k, v in self._categories.items() if v.frequency >= 1}

    def _ensure_category(self, name: str) -> Category:
        if name not in self._categories:
            self._categories[name] = Category(name=name)
        return self._categories[name]

    def _extract_price(self, item: ScrapedItem):
        if item.price:
            cat = self._ensure_category("price")
            cat.values.add(item.price)
            cat.frequency += 1

    def _extract_from_title(self, item: ScrapedItem):
        title_lower = item.title.lower()

        # Detect colours
        for colour in COLOUR_WORDS:
            if colour in title_lower.split():
                cat = self._ensure_category("colour")
                cat.values.add(colour.title())
                cat.frequency += 1

        # Detect sizes/specs
        size_matches = SIZE_PATTERN.findall(item.title)
        for match in size_matches:
            cat = self._ensure_category("size_or_spec")
            cat.values.add(match.strip())
            cat.frequency += 1

    def _extract_from_attributes(self, item: ScrapedItem):
        for key, value in item.raw_attributes.items():
            key_lower = key.lower().strip()

            if any(b in key_lower for b in BRAND_INDICATORS):
                cat = self._ensure_category("brand")
                cat.values.add(value.strip())
                cat.frequency += 1
            else:
                cat = self._ensure_category(key_lower)
                cat.values.add(value.strip())
                cat.frequency += 1

    def get_filter_options(self, items: list[ScrapedItem]) -> dict[str, list[str]]:
        categories = self.analyse_items(items)
        return {name: sorted(cat.values) for name, cat in categories.items()}
