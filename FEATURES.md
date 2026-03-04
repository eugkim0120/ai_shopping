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

## Planned
- [ ] Playwright-based scraping for JS-heavy sites
- [ ] Caching layer for search results
- [ ] User preferences and saved searches
- [ ] Price history tracking
- [ ] Additional marketplaces (Depop, Backmarket, etc.)
