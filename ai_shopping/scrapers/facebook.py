"""Facebook Marketplace scraper."""

from bs4 import BeautifulSoup

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem


class FacebookMarketplaceScraper(BaseScraper):
    name = "facebook_marketplace"
    BASE_URL = "https://www.facebook.com/marketplace/search"

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        client = await self.get_client()
        params = {"query": query}
        if "min_price" in filters:
            params["minPrice"] = filters["min_price"]
        if "max_price" in filters:
            params["maxPrice"] = filters["max_price"]

        try:
            resp = await client.get(self.BASE_URL, params=params)
            return self._parse_search_results(resp.text)
        except Exception:
            return []

    def _parse_search_results(self, html: str) -> list[ScrapedItem]:
        soup = BeautifulSoup(html, "lxml")
        items = []
        for card in soup.select("[data-testid='marketplace-search-result']"):
            title_el = card.select_one("span")
            price_el = card.select_one("[data-testid='marketplace-listing-price']")
            link_el = card.select_one("a")
            img_el = card.select_one("img")

            if not title_el:
                continue

            url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                url = href if href.startswith("http") else f"https://www.facebook.com{href}"

            items.append(
                ScrapedItem(
                    title=title_el.get_text(strip=True),
                    price=price_el.get_text(strip=True) if price_el else None,
                    url=url,
                    image_url=img_el["src"] if img_el and img_el.get("src") else "",
                    marketplace=self.name,
                )
            )
        return items

    async def extract_details(self, item_url: str) -> dict[str, str]:
        client = await self.get_client()
        try:
            resp = await client.get(item_url)
            soup = BeautifulSoup(resp.text, "lxml")
            details = {}
            for span in soup.select("span[dir='auto']"):
                text = span.get_text(strip=True)
                if ":" in text:
                    key, _, val = text.partition(":")
                    details[key.strip()] = val.strip()
            return details
        except Exception:
            return {}
