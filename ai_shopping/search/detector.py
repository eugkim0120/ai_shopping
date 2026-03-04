"""Search intent detector — parses natural language queries into structured search."""

import re
from dataclasses import dataclass, field


@dataclass
class SearchIntent:
    """Parsed search intent from a natural language query."""

    query: str
    min_price: float | None = None
    max_price: float | None = None
    colour: str | None = None
    brand: str | None = None
    condition: str | None = None
    material: str | None = None
    size: str | None = None
    marketplaces: list[str] = field(default_factory=list)
    raw_query: str = ""


PRICE_UNDER = re.compile(r"(?:under|below|less than|max|up to)\s*[£$€]?\s*([\d,]+)", re.I)
PRICE_OVER = re.compile(r"(?:over|above|more than|min|at least)\s*[£$€]?\s*([\d,]+)", re.I)
PRICE_RANGE = re.compile(r"[£$€]?\s*([\d,]+)\s*[-–to]+\s*[£$€]?\s*([\d,]+)", re.I)

COLOUR_WORDS = {
    "black", "white", "red", "blue", "green", "yellow", "orange", "purple",
    "pink", "grey", "gray", "brown", "silver", "gold", "navy", "beige",
    "neon", "cream",
}

CONDITION_WORDS = [
    "like new", "good condition", "refurbished",
    "secondhand", "second hand", "pre-owned", "preloved",
    "used", "new",
]

# Map informal condition words to standard ones for filtering
CONDITION_ALIASES = {
    "secondhand": "used",
    "second hand": "used",
    "pre-owned": "used",
    "preloved": "used",
    "vintage": "used",
}

MATERIAL_WORDS = {
    "leather", "cotton", "wool", "silk", "denim", "nylon",
    "rattan", "wood", "metal", "stainless steel",
}

BRAND_WORDS = {
    "apple", "samsung", "sony", "nike", "adidas", "dyson", "nintendo", "playstation",
    "xbox", "bose", "jbl", "dell", "lg", "philips", "oral-b", "tefal", "ninja",
    "nespresso", "sage", "levi's", "levis", "reebok", "puma", "the north face",
    "columbia", "superdry", "zara", "h&m", "michael kors", "coach", "ted baker",
    "casio", "seiko", "fossil", "timex", "ikea", "beats",
}

SIZE_PATTERN = re.compile(
    r"\bsize\s*(\d+(?:\.\d+)?)\b"
    r"|\b(\d+(?:\.\d+)?)\s*(?:inch|\")\b"
    r"|\b(XS|XXS|XXL|XL|S|M|L)\b",
    re.I,
)

MARKETPLACE_ALIASES = {
    "amazon": "amazon", "ebay": "ebay", "gumtree": "gumtree",
    "facebook marketplace": "facebook_marketplace",
    "facebook": "facebook_marketplace", "fb marketplace": "facebook_marketplace",
    "fb": "facebook_marketplace", "vinted": "vinted",
}


class SearchDetector:
    """Parses a natural language search query into structured filters."""

    def parse(self, raw_query: str) -> SearchIntent:
        intent = SearchIntent(query=raw_query, raw_query=raw_query)
        text = raw_query.lower()

        self._extract_prices(text, intent)
        self._extract_condition(text, intent)
        self._extract_brand(text, intent)
        self._extract_material(text, intent)
        self._extract_size(text, intent)
        self._extract_colour(text, intent)
        self._extract_marketplaces(text, intent)
        intent.query = self._clean_query(text, intent)

        return intent

    def _extract_prices(self, text: str, intent: SearchIntent):
        range_match = PRICE_RANGE.search(text)
        if range_match:
            intent.min_price = float(range_match.group(1).replace(",", ""))
            intent.max_price = float(range_match.group(2).replace(",", ""))
            return

        under_match = PRICE_UNDER.search(text)
        if under_match:
            intent.max_price = float(under_match.group(1).replace(",", ""))

        over_match = PRICE_OVER.search(text)
        if over_match:
            intent.min_price = float(over_match.group(1).replace(",", ""))

    def _extract_colour(self, text: str, intent: SearchIntent):
        for colour in COLOUR_WORDS:
            if re.search(rf"\b{colour}\b", text):
                intent.colour = colour
                return

    def _extract_condition(self, text: str, intent: SearchIntent):
        for condition in CONDITION_WORDS:
            if condition in text:
                # Normalize informal terms to standard condition
                intent.condition = CONDITION_ALIASES.get(
                    condition, condition,
                )
                return
        # Also check "vintage" as implicit condition
        if "vintage" in text:
            intent.condition = "used"

    def _extract_brand(self, text: str, intent: SearchIntent):
        for brand in sorted(BRAND_WORDS, key=len, reverse=True):
            if brand in text:
                intent.brand = brand
                return

    def _extract_material(self, text: str, intent: SearchIntent):
        for material in MATERIAL_WORDS:
            if re.search(rf"\b{material}\b", text):
                intent.material = material
                return

    def _extract_size(self, text: str, intent: SearchIntent):
        match = SIZE_PATTERN.search(text)
        if match:
            intent.size = next(g for g in match.groups() if g is not None)

    def _extract_marketplaces(self, text: str, intent: SearchIntent):
        for alias in sorted(MARKETPLACE_ALIASES.keys(), key=len, reverse=True):
            if alias in text:
                name = MARKETPLACE_ALIASES[alias]
                if name not in intent.marketplaces:
                    intent.marketplaces.append(name)

    def _clean_query(self, text: str, intent: SearchIntent) -> str:
        cleaned = text
        for pattern in [PRICE_UNDER, PRICE_OVER, PRICE_RANGE]:
            cleaned = pattern.sub("", cleaned)

        if intent.condition:
            cleaned = cleaned.replace(intent.condition, "")

        for alias in sorted(MARKETPLACE_ALIASES.keys(), key=len, reverse=True):
            cleaned = cleaned.replace(alias, "")

        # Only strip filler words at word boundaries and only when standalone
        cleaned = re.sub(r"\bon\s*$", "", cleaned)
        cleaned = re.sub(r"\bfrom\s*$", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned
