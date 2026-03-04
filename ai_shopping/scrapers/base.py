"""Base scraper abstraction — all marketplace scrapers implement this interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import httpx


@dataclass
class ScrapedItem:
    """A single item scraped from a marketplace."""

    title: str
    price: str | None = None
    url: str = ""
    image_url: str = ""
    marketplace: str = ""
    raw_attributes: dict[str, str] = field(default_factory=dict)


class BaseScraper(ABC):
    """Abstract base for all marketplace scrapers."""

    name: str = "base"

    def __init__(self, config: dict | None = None):
        self.config = config or {}
        self._client: httpx.AsyncClient | None = None

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                headers={"User-Agent": self.config.get("user_agent", "AI-Shopping/0.1")},
                follow_redirects=True,
            )
        return self._client

    @abstractmethod
    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        """Search this marketplace for items matching the query."""

    @abstractmethod
    async def extract_details(self, item_url: str) -> dict[str, str]:
        """Extract detailed attributes from a single item page."""

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
