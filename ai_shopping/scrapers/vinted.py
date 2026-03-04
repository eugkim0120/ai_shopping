"""Vinted marketplace scraper."""

from bs4 import BeautifulSoup

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem


class VintedScraper(BaseScraper):
    name = "vinted"
    BASE_URL = "https://www.vinted.co.uk/catalog"

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        client = await self.get_client()
        params = {"search_text": query}
        if "min_price" in filters:
            params["price_from"] = filters["min_price"]
        if "max_price" in filters:
            params["price_to"] = filters["max_price"]

        resp = await client.get(self.BASE_URL, params=params)
        return self._parse_search_results(resp.text)

    def _parse_search_results(self, html: str) -> list[ScrapedItem]:
        soup = BeautifulSoup(html, "lxml")
        items = []
        for card in soup.select("[data-testid='grid-item']"):
            title_el = card.select_one("[data-testid='description-title']")
            price_el = card.select_one("[data-testid='price-text']")
            link_el = card.select_one("a")
            img_el = card.select_one("img")

            if not title_el:
                continue

            url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                url = href if href.startswith("http") else f"https://www.vinted.co.uk{href}"

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
        resp = await client.get(item_url)
        soup = BeautifulSoup(resp.text, "lxml")
        details = {}
        for row in soup.select("[data-testid='item-attributes'] .details-list__item"):
            key = row.select_one(".details-list__item-title")
            val = row.select_one(".details-list__item-value")
            if key and val:
                details[key.get_text(strip=True)] = val.get_text(strip=True)
        return details
