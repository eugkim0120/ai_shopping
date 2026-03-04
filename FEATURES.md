# Features Tracker

## v0.1.0 — Project Foundation
- [x] README.md with project description
- [x] CLAUDE.md with engineering guidelines
- [x] Project structure and versioning

## v0.2.0 — Core Implementation
- [x] Base scraper abstraction
- [x] Amazon scraper
- [x] eBay scraper
- [x] Facebook Marketplace scraper
- [x] GumTree scraper
- [x] Vinted scraper
- [x] Scraper registry and factory
- [x] Dynamic category extraction
- [x] Product-type-aware categorisation (colour, brand, size/spec, price)
- [x] Configurable category rules
- [x] Natural language search parsing
- [x] Intent detection (price, colour, condition, marketplace)
- [x] Multi-marketplace search orchestration
- [x] FastAPI backend API
- [x] Frontend with search interface
- [x] Results display with dynamic categories
- [x] Responsive, polished dark-theme design
- [x] Full test suite (23 tests passing)

## v0.3.0 — Demo Fallback & Search Enhancement (Iteration 1)
- [x] Demo data provider with ~75 realistic products across 5 marketplaces
- [x] Automatic fallback to demo data when live scrapers fail
- [x] Enhanced brand detection (30+ brands)
- [x] Material and size extraction in search intent
- [x] Working dynamic filters in frontend
- [x] Sort by price/name in API and frontend
- [x] Condition-coloured badges (new/used/refurbished/like-new)
- [x] Info-level error styling for demo mode notices
- [x] Test suite expanded to 35 tests

## v0.4.0 — Relevance & UX Polish (Iteration 2)
- [x] Improved scoring: minimum match ratio (40%), stop word filtering
- [x] Word-boundary matching with prefix support
- [x] Multi-word phrase bonus in relevance scoring
- [x] Demo mode banner visible when using fallback data
- [x] Filter count shows "X of Y results" with live updates
- [x] Clear All Filters button in filter panel
- [x] Sort persists when filters change
- [x] Dramatically improved search relevance across all 20 test queries

## v0.5.0 — Real Web Data, Synonym Matching & Smart Filtering (Iterations 3 & 4)
- [x] WebDataScraper with ~160 real products sourced from live web searches
- [x] Real prices from Amazon, eBay, Gumtree, Facebook Marketplace & Vinted (March 2026)
- [x] Synonym expansion (pushchair↔stroller↔pram, trainers↔sneakers, etc.)
- [x] Hard brand filtering — brand in query rejects non-matching items
- [x] Type-aware conflict filtering (earbuds vs headphones vs speakers)
- [x] Dynamic minimum match ratio (0.6 for short queries, 0.5 for longer)
- [x] Relevance-first sort order (score-based, not price-based)
- [x] Marketplace colour-coded badges (Amazon orange, eBay blue, etc.)
- [x] Marketplace chips wired to API — deselect to filter by marketplace
- [x] Data freshness indicator ("Prices sourced from... — March 2026")
- [x] 20/20 search queries return relevant results
- [x] Test suite expanded to 44 tests

## Planned
- [ ] Playwright-based scraping for JS-heavy sites
- [ ] Caching layer for search results
- [ ] User preferences and saved searches
- [ ] Price history tracking
- [ ] Additional marketplaces (Depop, Backmarket, etc.)
