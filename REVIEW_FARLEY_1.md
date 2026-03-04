# David Farley Code Review — Iteration 1
**Reviewer perspective**: Author of *Modern Software Engineering*, *Continuous Delivery*
**Rating**: 5.5/10

## What Works Well
- Clean separation of concerns: scraper layer, search layer, categorisation, web layer
- BaseScraper ABC gives a clear contract — good use of abstraction
- Async throughout — correct use of asyncio.gather for concurrent marketplace search
- Tests exist and run fast (1.5s for 44 tests)
- ScrapedItem dataclass is a clean, immutable-ish data transfer object

## Critical Issues

### 1. MASSIVE Duplication Between DemoScraper and WebDataScraper (DRY Violation)
The `_score_item()` function is **duplicated wholesale** between `demo.py` and `web_data.py`.
The `_price_to_float()` function is **triplicated** — it exists in `demo.py`, `web_data.py`, AND `api.py`.

This is the single biggest design flaw. When scoring logic evolves (and it has — synonyms,
brand filtering, type conflicts were only added to web_data.py), you now have TWO divergent
scoring implementations. This violates the fundamental principle: every piece of knowledge
should have a single, unambiguous representation in the system.

**Fix**: Extract a shared `scoring.py` module. Both scrapers delegate to it.

### 2. 400+ Lines of Hardcoded Data in Source Files
`web_data.py` has ~160 product dicts hardcoded as Python literals. `demo.py` has another ~75.
This is data masquerading as code. It bloats source files, makes diffs noisy, and tangles
data changes with logic changes.

**Fix**: Move catalogue data to JSON files under a `data/` directory. Load at import time.
This separates concerns: data vs. logic. Makes the data independently testable and versionable.

### 3. `_parse_price()` Exists Three Times
Three separate implementations of price parsing across the codebase. Each slightly different:
- `demo.py:_price_to_float()` — returns None on failure
- `web_data.py:_price_to_float()` — returns None on failure
- `api.py:_parse_price()` — returns None on failure
- `orchestrator.py:_parse_price()` — returns float("inf") on failure

Four implementations, two different failure semantics. This will cause bugs.

**Fix**: Single `parse_price()` in a shared utility module.

### 4. Tests Are Too Shallow — They Test Structure, Not Behaviour
Look at `test_web_data.py`:
```python
async def test_condition_filter(ebay_web):
    results = await ebay_web.search("headphones", condition="refurbished")
    assert isinstance(results, list)
```
This test asserts *nothing about behaviour*. It only checks the return type. Any function
returning `[]` would pass. Tests should verify that condition filtering actually works —
that refurbished items are included and non-refurbished items are excluded.

Similarly, `test_search_returns_real_products` uses `>= 50%` as a threshold, which is a
weak assertion for a relevance system.

**Fix**: Tests should assert specific, observable behaviour. "Given these products and this
query, exactly these items should match."

### 5. WebDataScraper Inherits BaseScraper But Doesn't Need HTTP
`WebDataScraper` extends `BaseScraper` which creates an `httpx.AsyncClient`. But WebDataScraper
never makes HTTP requests — it searches in-memory data. It inherits a `get_client()` method
it will never use, and a `close()` method that cleans up a client that was never created.

This violates the Interface Segregation Principle and creates confusion about what this
class actually does.

**Fix**: Extract a `Searcher` protocol/interface with just `search()` and `extract_details()`.
BaseScraper can implement it with HTTP; WebDataScraper implements it without.

### 6. Scoring Algorithm Is a God Function
`_score_item()` in `web_data.py` (lines 224-310) does brand filtering, synonym expansion,
word matching, phrase detection, type-conflict filtering, colour matching, and condition
matching — all in a single 86-line function.

This is hard to test in isolation. Each scoring concern should be independently testable.

**Fix**: Decompose into small, focused scoring functions. Each can be unit tested independently.

### 7. No Tests for Scoring Logic
The most critical business logic — the scoring algorithm — has ZERO direct unit tests.
It's only tested indirectly through the scraper search method. This means:
- Can't tell if a scoring bug is in scoring or in filtering
- Can't test edge cases without constructing full product catalogues
- Can't regression-test specific scoring scenarios

**Fix**: Direct unit tests for `_score_item()`, `_expand_synonyms()`, type conflict detection.

### 8. Unused Dead Code in Orchestrator
`orchestrator.py` has a `_parse_price()` function at module level (lines 112-117) that is
never called from anywhere. Dead code is noise.

**Fix**: Delete it.

## Minor Issues
- `app.py` line 46: `version="0.1.0"` but project is at 0.5.0
- `import random` in demo.py is unused
- `from dataclasses import field` in demo.py is unused
- Synonym groups in web_data.py overlap: "earphones" appears in both headphones AND earbuds groups

## Summary
The architecture has good bones — clean layers, clear responsibilities, async patterns. But
the codebase has accumulated significant accidental complexity through duplication, hardcoded
data, and insufficiently tested scoring logic. The most critical path (relevance scoring) is
the least tested and most duplicated part of the system. Fix the duplication, extract the data,
test the scoring, and this becomes a much more maintainable system.
