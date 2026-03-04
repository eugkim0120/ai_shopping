# Customer Feedback — Iteration 1
**Date:** 2026-03-04
**Tester Role:** Critical end-user testing 20 everyday item searches

## Overall Rating: 1/10 — UNUSABLE

## Critical Issues (Show-Stoppers)

### 1. ZERO RESULTS FOR EVERY SEARCH — Severity: CRITICAL
Every single one of my 20 searches returned 0 results. The tool is completely non-functional as a shopping tool. All 5 marketplace scrapers get 403 Forbidden errors because:
- Direct HTTP GET requests to Amazon/eBay/Gumtree/Facebook/Vinted are blocked by anti-bot measures
- No browser fingerprinting, no cookie handling, no JavaScript rendering
- These sites require proper headers, sessions, or browser automation (Playwright/Selenium)
- **Verdict:** The core value proposition of the product is broken. It scrapes nothing.

### 2. NO FALLBACK OR GRACEFUL DEGRADATION — Severity: HIGH
When all scrapers fail, the user sees an empty page with a vague "Warnings" line. There's no helpful message like "We couldn't reach Amazon right now, try again" or "Results may be limited." The errors are raw Python exception strings shown to the user (e.g., "amazon: 403 Forbidden"). That's a developer error dump, not a user-facing message.

### 3. SCRAPER ERRORS ARE SILENT IN UI — Severity: HIGH
The error line is a tiny red bar that's easy to miss. If I searched for "wireless headphones" and got 0 results with 4 errors, I'd think the product just doesn't work — I wouldn't understand that 4 out of 5 scrapers failed. There's no per-marketplace status indicator.

## Major Issues

### 4. NO ERROR RECOVERY OR RETRY — Severity: MEDIUM
If Amazon returns a 403, the scraper just gives up. No retry with different headers, no exponential backoff, no cached results, nothing. One transient failure = total failure.

### 5. SEARCH INTENT DETECTION IS TOO BASIC — Severity: MEDIUM
- "4K monitor 27 inch" — doesn't detect "4K" as a spec or "27 inch" as a size
- "protein powder chocolate" — doesn't detect "chocolate" as a flavour
- "women's handbag leather" — doesn't detect "leather" as a material
- "gold watch" — detects "gold" as a colour rather than potentially a material
- No brand detection in queries (Samsung, Apple, Nike, Dyson, PlayStation)
- The query cleaning strips too aggressively — "on", "from", "in", "the" are removed even when they're part of product names

### 6. MARKETPLACE CHIPS DON'T ACTUALLY FILTER — Severity: MEDIUM
The HTML has marketplace checkboxes but the JavaScript doesn't actually use them when making API calls. Unchecking "amazon" still sends the search to all marketplaces.

### 7. DYNAMIC FILTERS DO NOTHING — Severity: MEDIUM
The checkbox filters in the sidebar are rendered but `applyFilters()` in app.js is a no-op — it just sets `display: ''` on all cards. Checking/unchecking filters has zero effect.

## Minor Issues

### 8. NO SORTING — Severity: LOW
Can't sort by price, relevance, recency. For a shopping tool, sorting by price (low to high) is table stakes.

### 9. NO PAGINATION — Severity: LOW
If results eventually work, there's no pagination or infinite scroll. All results dump into one page.

### 10. VERSION MISMATCH IN FOOTER
Footer says "v0.1.0" but the project is at v0.2.0.

### 11. NO LOADING TIMEOUT
The spinner just spins forever if something hangs. No timeout message.

### 12. SEARCH HISTORY / RECENT SEARCHES MISSING
No way to see previous searches or quickly re-run them.

## What Does Work (Barely)

- The UI design is actually nice — dark theme, clean layout, responsive
- The search intent parser correctly extracts: price ranges, colours, conditions, marketplace names
- The architecture (registry, orchestrator, categoriser) is well-structured
- API endpoints respond quickly (the 403s come back fast at least)
- The 23 unit tests all pass

## Summary

This is a **well-architected prototype with zero actual functionality**. The skeleton is good, the tests are passing, the UI looks great — but the core value proposition (scraping real marketplaces) is completely broken. It's like a beautiful car with no engine.

**Priority fixes needed:**
1. Make at least ONE scraper actually return real results (eBay is most likely to work with proper headers)
2. Add proper error handling with user-friendly messages
3. Make the marketplace chips and dynamic filters actually work
4. Add sorting
