"""Shared utilities — single source of truth for common operations."""


def parse_price(price_str: str | None) -> float | None:
    """Parse a price string like '£129.99' into a float. Returns None on failure."""
    if not price_str:
        return None
    try:
        cleaned = (
            price_str.replace("£", "").replace("$", "")
            .replace("€", "").replace(",", "").strip()
        )
        return float(cleaned)
    except (ValueError, AttributeError):
        return None
