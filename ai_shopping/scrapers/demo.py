"""Demo data provider — returns realistic mock results for development and testing.

Used as a fallback when real scrapers fail, or as the primary data source during
development. Generates plausible products with attributes that exercise the full
categorisation and filtering pipeline.
"""

import hashlib
import random
from dataclasses import field

from ai_shopping.scrapers.base import BaseScraper, ScrapedItem

# Realistic product catalogues per marketplace
_CATALOGUES: dict[str, list[dict]] = {
    "amazon": [
        {"title": "Sony WH-1000XM5 Wireless Noise Cancelling Headphones - Black", "price": "£289.00", "attrs": {"brand": "Sony", "colour": "Black", "connectivity": "Bluetooth 5.2"}},
        {"title": "Apple AirPods Pro 2nd Generation with MagSafe Case", "price": "£229.00", "attrs": {"brand": "Apple", "colour": "White", "connectivity": "Bluetooth 5.3"}},
        {"title": "Samsung Galaxy S24 Ultra 256GB Titanium Black Unlocked", "price": "£1,149.00", "attrs": {"brand": "Samsung", "colour": "Black", "storage": "256GB", "condition": "New"}},
        {"title": "Apple iPhone 15 Pro Max 256GB Natural Titanium", "price": "£1,199.00", "attrs": {"brand": "Apple", "colour": "Natural Titanium", "storage": "256GB"}},
        {"title": "Nike Air Max 90 Men's Running Shoes - White/Black Size 10", "price": "£129.99", "attrs": {"brand": "Nike", "colour": "White", "size": "10", "type": "Running Shoes"}},
        {"title": "Ninja AF300UK Air Fryer MAX 5.2L - Grey", "price": "£99.99", "attrs": {"brand": "Ninja", "colour": "Grey", "capacity": "5.2L"}},
        {"title": "De'Longhi Magnifica S Bean to Cup Coffee Machine - Silver", "price": "£299.00", "attrs": {"brand": "De'Longhi", "colour": "Silver", "type": "Bean to Cup"}},
        {"title": "Dyson V15 Detect Absolute Cordless Vacuum Cleaner", "price": "£599.99", "attrs": {"brand": "Dyson", "colour": "Yellow", "type": "Cordless", "condition": "New"}},
        {"title": "LG 27GP850-B 27 Inch QHD Nano IPS Gaming Monitor", "price": "£349.99", "attrs": {"brand": "LG", "size": "27 inch", "resolution": "QHD", "panel": "Nano IPS"}},
        {"title": "Optimum Nutrition Gold Standard Whey Protein Chocolate 2.27kg", "price": "£44.99", "attrs": {"brand": "Optimum Nutrition", "flavour": "Chocolate", "weight": "2.27kg"}},
        {"title": "Levi's 501 Original Fit Men's Jeans - Blue Size 32", "price": "£69.99", "attrs": {"brand": "Levi's", "colour": "Blue", "size": "32", "type": "Jeans"}},
        {"title": "Nintendo Switch OLED Model - White", "price": "£309.99", "attrs": {"brand": "Nintendo", "colour": "White", "storage": "64GB"}},
        {"title": "Oral-B iO Series 9 Electric Toothbrush - Black Onyx", "price": "£249.99", "attrs": {"brand": "Oral-B", "colour": "Black", "type": "Electric Toothbrush"}},
        {"title": "Gaiam Essentials Thick Yoga Mat - Purple 6mm", "price": "£24.99", "attrs": {"brand": "Gaiam", "colour": "Purple", "thickness": "6mm"}},
        {"title": "Sony DualSense Wireless Controller for PS5 - White", "price": "£59.99", "attrs": {"brand": "Sony", "colour": "White", "type": "PS5 Controller"}},
        {"title": "Casio G-Shock Men's Watch Gold Tone", "price": "£89.99", "attrs": {"brand": "Casio", "colour": "Gold", "type": "Watch"}},
        {"title": "Samsung 4K Smart Monitor M8 32 Inch - White", "price": "£549.00", "attrs": {"brand": "Samsung", "size": "32 inch", "resolution": "4K", "colour": "White"}},
        {"title": "LED Desk Lamp with USB Charging Port - Dimmable White", "price": "£29.99", "attrs": {"colour": "White", "type": "Desk Lamp", "feature": "USB Charging"}},
        {"title": "Fiskars Kids Bicycle 16 inch - Red", "price": "£149.99", "attrs": {"brand": "Fiskars", "colour": "Red", "size": "16 inch", "type": "Kids Bicycle"}},
        {"title": "Keter Garden Furniture Set 4 Piece - Graphite", "price": "£399.99", "attrs": {"brand": "Keter", "colour": "Graphite", "type": "Garden Furniture", "pieces": "4"}},
    ],
    "ebay": [
        {"title": "Bose QuietComfort 45 Wireless Headphones - White Smoke", "price": "£199.99", "attrs": {"brand": "Bose", "colour": "White", "condition": "New"}},
        {"title": "iPhone 15 Pro Max 256GB Blue Titanium - Unlocked USED", "price": "£849.00", "attrs": {"brand": "Apple", "colour": "Blue", "storage": "256GB", "condition": "Used"}},
        {"title": "Samsung Galaxy S24 128GB - Refurbished Good", "price": "£449.99", "attrs": {"brand": "Samsung", "storage": "128GB", "condition": "Refurbished"}},
        {"title": "Adidas Ultraboost 22 Running Shoes Black Size 10", "price": "£89.99", "attrs": {"brand": "Adidas", "colour": "Black", "size": "10", "condition": "New"}},
        {"title": "Tefal ActiFry Genius XL Air Fryer 1.7kg - Black", "price": "£149.00", "attrs": {"brand": "Tefal", "colour": "Black", "capacity": "1.7kg"}},
        {"title": "Nespresso Vertuo Next Coffee Machine - Red", "price": "£79.99", "attrs": {"brand": "Nespresso", "colour": "Red", "condition": "Like New"}},
        {"title": "Dyson V11 Absolute Cordless Vacuum - Refurbished", "price": "£299.99", "attrs": {"brand": "Dyson", "colour": "Purple", "condition": "Refurbished"}},
        {"title": "Dell S2722QC 27\" 4K USB-C Monitor", "price": "£279.99", "attrs": {"brand": "Dell", "size": "27 inch", "resolution": "4K"}},
        {"title": "MyProtein Impact Whey Protein Chocolate Smooth 5kg", "price": "£52.99", "attrs": {"brand": "MyProtein", "flavour": "Chocolate", "weight": "5kg"}},
        {"title": "Wrangler Texas Men's Jeans Blue Size 32x32", "price": "£39.99", "attrs": {"brand": "Wrangler", "colour": "Blue", "size": "32", "type": "Jeans"}},
        {"title": "Nintendo Switch OLED Neon - Boxed Like New", "price": "£269.00", "attrs": {"brand": "Nintendo", "colour": "Neon", "condition": "Like New"}},
        {"title": "Philips Sonicare DiamondClean Electric Toothbrush", "price": "£129.99", "attrs": {"brand": "Philips", "colour": "White", "type": "Electric Toothbrush"}},
        {"title": "Manduka PRO Yoga Mat 6mm - Black", "price": "£89.00", "attrs": {"brand": "Manduka", "colour": "Black", "thickness": "6mm"}},
        {"title": "PS5 DualSense Edge Wireless Controller - Black", "price": "£189.99", "attrs": {"brand": "Sony", "colour": "Black", "type": "PS5 Controller"}},
        {"title": "Seiko Presage Automatic Men's Watch Gold", "price": "£189.00", "attrs": {"brand": "Seiko", "colour": "Gold", "type": "Watch"}},
        {"title": "Kids Balance Bicycle 12 inch Pink", "price": "£49.99", "attrs": {"colour": "Pink", "size": "12 inch", "type": "Kids Bicycle"}},
        {"title": "Rattan Garden Furniture Set 5 Piece Brown", "price": "£299.99", "attrs": {"colour": "Brown", "type": "Garden Furniture", "pieces": "5", "material": "Rattan"}},
        {"title": "Michael Kors Jet Set Travel Leather Handbag - Brown", "price": "£159.00", "attrs": {"brand": "Michael Kors", "colour": "Brown", "material": "Leather", "type": "Handbag"}},
        {"title": "BenQ EW3270U 32\" 4K HDR Monitor", "price": "£329.99", "attrs": {"brand": "BenQ", "size": "32 inch", "resolution": "4K"}},
        {"title": "TaoTronics LED Desk Lamp Eye-Caring Silver", "price": "£24.99", "attrs": {"brand": "TaoTronics", "colour": "Silver", "type": "Desk Lamp"}},
    ],
    "gumtree": [
        {"title": "Sony WH-1000XM4 Headphones Barely Used", "price": "£150.00", "attrs": {"brand": "Sony", "colour": "Black", "condition": "Used"}},
        {"title": "iPhone 14 Pro 128GB Space Black - Good Condition", "price": "£550.00", "attrs": {"brand": "Apple", "colour": "Black", "storage": "128GB", "condition": "Good Condition"}},
        {"title": "Samsung Galaxy S23 Cream 256GB Unlocked", "price": "£380.00", "attrs": {"brand": "Samsung", "colour": "Cream", "storage": "256GB"}},
        {"title": "Nike Air Force 1 White Size 9 - Worn Once", "price": "£60.00", "attrs": {"brand": "Nike", "colour": "White", "size": "9", "condition": "Like New"}},
        {"title": "Cosori Air Fryer 5.5L Black", "price": "£45.00", "attrs": {"brand": "Cosori", "colour": "Black", "capacity": "5.5L"}},
        {"title": "Sage Barista Express Coffee Machine Silver", "price": "£350.00", "attrs": {"brand": "Sage", "colour": "Silver", "type": "Coffee Machine", "condition": "Used"}},
        {"title": "Kids Bicycle 20 Inch Blue - Collection Only", "price": "£40.00", "attrs": {"colour": "Blue", "size": "20 inch", "type": "Kids Bicycle"}},
        {"title": "IKEA MARKUS Office Chair Black", "price": "£80.00", "attrs": {"brand": "IKEA", "colour": "Black", "type": "Office Chair"}},
        {"title": "Yoga Mat 10mm Thick Blue with Carry Strap", "price": "£12.00", "attrs": {"colour": "Blue", "thickness": "10mm"}},
        {"title": "PS5 Disc Edition with 2 Controllers", "price": "£400.00", "attrs": {"brand": "Sony", "colour": "White", "condition": "Used"}},
        {"title": "Garden Table and 4 Chairs Set Wood", "price": "£120.00", "attrs": {"type": "Garden Furniture", "material": "Wood", "pieces": "5"}},
        {"title": "Coach Leather Handbag Black - Genuine", "price": "£95.00", "attrs": {"brand": "Coach", "colour": "Black", "material": "Leather", "type": "Handbag"}},
        {"title": "Men's Casio Watch Gold Tone Vintage", "price": "£35.00", "attrs": {"brand": "Casio", "colour": "Gold", "type": "Watch", "condition": "Used"}},
    ],
    "facebook_marketplace": [
        {"title": "Beats Solo3 Wireless Headphones Red", "price": "£70.00", "attrs": {"brand": "Beats", "colour": "Red", "condition": "Good Condition"}},
        {"title": "iPhone 13 Mini 128GB Green Unlocked", "price": "£320.00", "attrs": {"brand": "Apple", "colour": "Green", "storage": "128GB"}},
        {"title": "Reebok Running Shoes Size 10 Black", "price": "£25.00", "attrs": {"brand": "Reebok", "colour": "Black", "size": "10"}},
        {"title": "Tower Air Fryer 4L Grey - Like New", "price": "£30.00", "attrs": {"brand": "Tower", "colour": "Grey", "capacity": "4L", "condition": "Like New"}},
        {"title": "DeLonghi Dedica Coffee Machine Silver", "price": "£120.00", "attrs": {"brand": "DeLonghi", "colour": "Silver", "type": "Coffee Machine"}},
        {"title": "Kids Frozen Bicycle 14 inch Pink with Stabilisers", "price": "£35.00", "attrs": {"colour": "Pink", "size": "14 inch", "type": "Kids Bicycle"}},
        {"title": "Outdoor Rattan Sofa Set 3 Piece Grey", "price": "£180.00", "attrs": {"colour": "Grey", "type": "Garden Furniture", "material": "Rattan", "pieces": "3"}},
        {"title": "Dyson V8 Absolute Vacuum Cleaner", "price": "£150.00", "attrs": {"brand": "Dyson", "condition": "Used"}},
        {"title": "Nintendo Switch Lite Yellow", "price": "£130.00", "attrs": {"brand": "Nintendo", "colour": "Yellow"}},
        {"title": "Electric Toothbrush Oral-B Pro 3 Black", "price": "£25.00", "attrs": {"brand": "Oral-B", "colour": "Black", "type": "Electric Toothbrush"}},
        {"title": "Ted Baker Women's Leather Handbag Navy", "price": "£55.00", "attrs": {"brand": "Ted Baker", "colour": "Navy", "material": "Leather", "type": "Handbag"}},
        {"title": "Fossil Men's Watch Gold Stainless Steel", "price": "£65.00", "attrs": {"brand": "Fossil", "colour": "Gold", "material": "Stainless Steel", "type": "Watch"}},
    ],
    "vinted": [
        {"title": "JBL Tune 510BT Wireless Headphones Blue", "price": "£18.00", "attrs": {"brand": "JBL", "colour": "Blue", "condition": "Good Condition"}},
        {"title": "Nike Dunk Low Panda Size 10 - Used", "price": "£75.00", "attrs": {"brand": "Nike", "colour": "Black/White", "size": "10", "condition": "Used"}},
        {"title": "Levi's 511 Slim Fit Jeans Blue 32W", "price": "£22.00", "attrs": {"brand": "Levi's", "colour": "Blue", "size": "32", "type": "Jeans"}},
        {"title": "North Face Winter Jacket Black Size L", "price": "£65.00", "attrs": {"brand": "The North Face", "colour": "Black", "size": "L", "type": "Winter Jacket"}},
        {"title": "Columbia Winter Puffer Jacket Navy Size M", "price": "£45.00", "attrs": {"brand": "Columbia", "colour": "Navy", "size": "M", "type": "Winter Jacket"}},
        {"title": "Zara Leather Tote Handbag Black", "price": "£28.00", "attrs": {"brand": "Zara", "colour": "Black", "material": "Leather", "type": "Handbag"}},
        {"title": "H&M Faux Leather Handbag Brown", "price": "£12.00", "attrs": {"brand": "H&M", "colour": "Brown", "material": "Faux Leather", "type": "Handbag"}},
        {"title": "Superdry Winter Coat Women's Grey Size S", "price": "£40.00", "attrs": {"brand": "Superdry", "colour": "Grey", "size": "S"}},
        {"title": "Timex Men's Watch Silver Classic", "price": "£20.00", "attrs": {"brand": "Timex", "colour": "Silver", "type": "Watch"}},
        {"title": "Casio Vintage Watch Gold A168WG", "price": "£25.00", "attrs": {"brand": "Casio", "colour": "Gold", "type": "Watch"}},
    ],
}


STOP_WORDS = {"the", "a", "an", "and", "or", "for", "with", "on", "in", "to", "of", "is", "it"}

# Minimum percentage of query words that must match for an item to be included
MIN_MATCH_RATIO = 0.5


def _score_item(item: dict, query_words: list[str], colour: str | None, condition: str | None) -> float:
    """Score how well an item matches the search query. Returns 0 for irrelevant items."""
    title_lower = item["title"].lower()
    title_words = set(title_lower.split())
    attrs = item.get("attrs", {})
    attrs_text = " ".join(attrs.values()).lower()
    attrs_words = set(attrs_text.split())
    all_words = title_words | attrs_words

    # Filter out stop words from query
    meaningful_words = [w for w in query_words if w not in STOP_WORDS]
    if not meaningful_words:
        return 0.0

    score = 0.0
    matches = 0
    for word in meaningful_words:
        # Require word boundary matching — word must appear as a standalone token
        # or as a prefix of a token (e.g. "headphone" matches "headphones")
        title_match = any(w.startswith(word) or word.startswith(w) for w in title_words if len(w) > 2)
        attrs_match = any(w.startswith(word) or word.startswith(w) for w in attrs_words if len(w) > 2)

        if title_match:
            score += 2.0
            matches += 1
        elif attrs_match:
            score += 1.0
            matches += 1

    # Multi-word phrase bonus: if 2+ consecutive words match in title, big bonus
    if len(meaningful_words) >= 2:
        for i in range(len(meaningful_words) - 1):
            phrase = f"{meaningful_words[i]} {meaningful_words[i+1]}"
            if phrase in title_lower:
                score += 3.0

    # Require minimum match ratio
    match_ratio = matches / len(meaningful_words) if meaningful_words else 0
    if match_ratio < MIN_MATCH_RATIO:
        return 0.0

    # Colour and condition as bonus (not core relevance)
    if colour and colour.lower() in attrs_text:
        score += 1.0
    if condition:
        item_cond = attrs.get("condition", "").lower()
        if condition.lower() in item_cond:
            score += 1.0

    return score


def _price_to_float(price_str: str) -> float | None:
    try:
        cleaned = price_str.replace("£", "").replace("$", "").replace("€", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return None


class DemoScraper(BaseScraper):
    """Returns realistic mock data — used when real scrapers are unavailable."""

    name = "demo"

    def __init__(self, marketplace_name: str, config: dict | None = None):
        super().__init__(config)
        self.name = marketplace_name
        self._catalogue = _CATALOGUES.get(marketplace_name, [])

    async def search(self, query: str, **filters) -> list[ScrapedItem]:
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 1]

        min_price = filters.get("min_price")
        max_price = filters.get("max_price")
        colour = filters.get("colour")
        condition = filters.get("condition")

        scored = []
        for item in self._catalogue:
            score = _score_item(item, query_words, colour, condition)
            if score <= 0:
                continue

            # Apply price filters
            price_val = _price_to_float(item["price"])
            if price_val is not None:
                if min_price is not None and price_val < float(min_price):
                    continue
                if max_price is not None and price_val > float(max_price):
                    continue

            scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)

        items = []
        for score, item_data in scored:
            seed = hashlib.md5(item_data["title"].encode()).hexdigest()[:8]
            items.append(ScrapedItem(
                title=item_data["title"],
                price=item_data["price"],
                url=f"https://www.example.com/{self.name}/item/{seed}",
                image_url=f"https://picsum.photos/seed/{seed}/400/300",
                marketplace=self.name,
                raw_attributes=item_data.get("attrs", {}),
            ))

        return items

    async def extract_details(self, item_url: str) -> dict[str, str]:
        return {"source": "demo", "note": "This is demo data"}
