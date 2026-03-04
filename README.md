# AI Shopping — Multi-Marketplace Scraper & Search Engine

This project scrapes Facebook marketplace, GumTree, Amazon, eBay, Vinted, and many of the top tech marketplaces. It allows the user to search for items, and it will automatically detect what it's asking for. The categorisation will not be pre-set, but automatically found (categorisation meaning e.g. brand, price, colour, specs, etc.) in a super configurable way, and that adjusts for product. The website UI should be impeccable.

## Features

- **Multi-Marketplace Scraping** — Facebook Marketplace, GumTree, Amazon, eBay, Vinted, and more
- **Intelligent Search** — Automatically detects what the user is looking for
- **Auto-Categorisation** — Dynamically discovers categories (brand, price, colour, specs, etc.) per product type
- **Super Configurable** — Fully adjustable scraping, categorisation, and display settings
- **Impeccable UI** — Clean, fast, responsive web interface

## Quick Start

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Start the application
uv run python -m ai_shopping
```

## Architecture

```
ai_shopping/
├── scrapers/         # Marketplace-specific scrapers
├── categorisation/   # Auto-categorisation engine
├── search/           # Search & intent detection
├── web/              # FastAPI backend + frontend
├── config/           # Configuration system
└── tests/            # Test suite
```

## Versioning

See `version.txt` for the current version. Tags follow semver: `v0.1.0`, `v0.2.0`, etc.
