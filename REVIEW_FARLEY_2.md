# David Farley Code Review — Iteration 2
**Reviewer perspective**: Author of *Modern Software Engineering*, *Continuous Delivery*
**Rating**: 7.5/10 (up from 5.5)

## What Improved
The team addressed several critical issues from the first review:
- **Single scoring module** (`scoring.py`) eliminates the worst duplication
- **Data extracted to JSON** — catalogue data no longer bloats source files
- **Shared `parse_price()`** — one function, one behaviour, everywhere
- **Dead code removed** — `_parse_price()` in orchestrator deleted
- **37 new tests** — scoring module now has direct unit tests for every function
- **Lint clean** — ruff passes with zero warnings
- **Shallow tests fixed** — condition filter test now asserts behaviour, not type

## Remaining Issues

### 1. DemoScraper and WebDataScraper Still Have Identical `search()` Methods
The `search()` method bodies in `demo.py` and `web_data.py` are **character-for-character
identical** (lines 40-78 in both files). The only differences between the two classes are:
- The JSON file they load
- The URL template for items
- The `extract_details()` return value

This is a textbook case for a Template Method or for extracting a shared base class.

**Fix**: Create a `CatalogueScraper` base class that both inherit from.

### 2. Global Mutable State in Catalogue Loading
Both `_load_catalogues()` functions use `global` mutable dicts. This creates hidden state
that persists across test runs, meaning tests can't be truly isolated. If a test modifies
the catalogue, all subsequent tests see the mutation.

**Fix**: Move catalogue loading into the scraper constructor. Pass data as a dependency.

### 3. BaseScraper Still Creates HTTP Clients for In-Memory Scrapers
The ISP violation from review 1 remains. Both DemoScraper and WebDataScraper call
`super().__init__()` which manages an httpx client they never use.

**Fix**: Extract a `Searcher` Protocol. Let both catalogue-based scrapers implement
it directly without inheriting HTTP machinery. Lower priority since it works, but
it's conceptually misleading.

### 4. Missing Integration Test: Orchestrator End-to-End
There are no tests verifying that the orchestrator correctly:
- Falls back to WebDataScraper when live scrapers fail
- Passes brand filter through to demo scrapers
- Aggregates results from multiple marketplaces

These are critical business flows with zero automated coverage.

**Fix**: Add integration tests for the orchestrator with controlled scraper behaviour.

## Summary
The codebase has improved significantly. The scoring logic is now testable and tested,
data is separated from logic, and there's no more quadrupled price parsing. The main
remaining debt is the identical `search()` method duplication between the two catalogue
scrapers — extract a shared base to eliminate it.

Rating: 7.5/10 — the architecture now follows the key principles of modularity,
testability, and single source of truth. The remaining issues are lower-severity.
