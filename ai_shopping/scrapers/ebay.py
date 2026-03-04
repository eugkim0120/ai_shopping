"""eBay marketplace scraper."""

from bs4 import BeautifulSoup

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem


class EbayScraper(BaseScraper):
    name = "ebay"
    BASE_URL = "https://www.ebay.co.uk/sch/i.html"

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        client = await self.get_client()
        params = {"_nkw": query, "_sacat": "0"}
        if "min_price" in filters:
            params["_udlo"] = filters["min_price"]
        if "max_price" in filters:
            params["_udhi"] = filters["max_price"]

        resp = await client.get(self.BASE_URL, params=params)
        return self._parse_search_results(resp.text)

    def _parse_search_results(self, html: str) -> list[ScrapedItem]:
        soup = BeautifulSoup(html, "lxml")
        items = []
        for card in soup.select(".s-item"):
            title_el = card.select_one(".s-item__title")
            price_el = card.select_one(".s-item__price")
            link_el = card.select_one(".s-item__link")
            img_el = card.select_one(".s-item__image-img")

            if not title_el or title_el.get_text(strip=True) == "Shop on eBay":
                continue

            items.append(
                ScrapedItem(
                    title=title_el.get_text(strip=True),
                    price=price_el.get_text(strip=True) if price_el else None,
                    url=link_el["href"] if link_el and link_el.get("href") else "",
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
        for row in soup.select(".ux-labels-values__labels-content"):
            label = row.select_one(".ux-labels-values__labels")
            value = row.select_one(".ux-labels-values__values")
            if label and value:
                details[label.get_text(strip=True)] = value.get_text(strip=True)
        return details
