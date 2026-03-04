"""Amazon marketplace scraper."""

from bs4 import BeautifulSoup

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem


class AmazonScraper(BaseScraper):
    name = "amazon"
    BASE_URL = "https://www.amazon.co.uk/s"

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        client = await self.get_client()
        params = {"k": query}
        if "min_price" in filters:
            params["low-price"] = filters["min_price"]
        if "max_price" in filters:
            params["high-price"] = filters["max_price"]

        resp = await client.get(self.BASE_URL, params=params)
        return self._parse_search_results(resp.text)

    def _parse_search_results(self, html: str) -> list[ScrapedItem]:
        soup = BeautifulSoup(html, "lxml")
        items = []
        for card in soup.select("[data-component-type='s-search-result']"):
            title_el = card.select_one("h2 a span")
            price_el = card.select_one(".a-price .a-offscreen")
            link_el = card.select_one("h2 a")
            img_el = card.select_one("img.s-image")

            if not title_el:
                continue

            url = ""
            if link_el and link_el.get("href"):
                url = "https://www.amazon.co.uk" + link_el["href"]

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
        for row in soup.select("#productDetails_techSpec_section_1 tr"):
            key = row.select_one("th")
            val = row.select_one("td")
            if key and val:
                details[key.get_text(strip=True)] = val.get_text(strip=True)
        return details
