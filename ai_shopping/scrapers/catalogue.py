"""Catalogue-based scraper — shared base for scrapers backed by in-memory data."""

import hashlib

from ai_shopping.scoring import has_budget_intent, score_item
from ai_shopping.scrapers.base import BaseScraper, ScrapedItem
from ai_shopping.utils import parse_price


class CatalogueScraper(BaseScraper):
    """Base class for scrapers that search an in-memory product catalogue.

    Subclasses provide the catalogue data and URL generation strategy.
    """

    name = "catalogue"

    def __init__(
        self,
        marketplace_name: str,
        catalogue: list[dict],
        config: dict | None = None,
    ):
        super().__init__(config)
        self.name = marketplace_name
        self._catalogue = catalogue

    def _item_url(self, item_data: dict, seed: str) -> str:
        """Generate the URL for an item. Override in subclasses."""
        return f"https://www.example.com/{self.name}/item/{seed}"

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        query_words = [w for w in query.lower().split() if len(w) > 1]

        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        colour = filters.get("colour")
        condition = filters.get("condition")
        brand = filters.get("brand")

        scored = []
        for item in self._catalogue:
            s = score_item(item, query_words, colour, condition, brand)
            if s <= 0:
                continue

            price_val = parse_price(item["price"])
            if price_val is not None:
                if min_price is not None and price_val < float(min_price):
                    continue
                if max_price is not None and price_val > float(max_price):
                    continue

            scored.append((s, item))

        # Budget-aware sorting: when user wants cheap, sort primarily by
        # relevance but use price as tiebreaker (cheaper first)
        if has_budget_intent(query_words):
            scored.sort(
                key=lambda x: (
                    -x[0],
                    parse_price(x[1]["price"]) or float("inf"),
                ),
            )
        else:
            scored.sort(key=lambda x: x[0], reverse=True)

        items = []
        for _, item_data in scored:
            seed = hashlib.md5(
                item_data["title"].encode(),
            ).hexdigest()[:8]
            items.append(ScrapedItem(
                title=item_data["title"],
                price=item_data["price"],
                url=self._item_url(item_data, seed),
                image_url=f"https://picsum.photos/seed/{seed}/400/300",
                marketplace=self.name,
                raw_attributes=item_data.get("attrs", {}),
            ))

        return items

    async def extract_details(self, item_url: str) -> dict[str, str]:
        return {"source": self.name}
