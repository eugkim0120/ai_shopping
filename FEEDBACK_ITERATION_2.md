# Customer Feedback — Iteration 2
**Date:** 2026-03-04
**Tester Role:** Critical end-user re-testing after iteration 1 fixes
**Version:** v0.3.0

## Overall Rating: 5/10 — FUNCTIONAL BUT ROUGH

Massive improvement from 1/10. The tool now returns results for all 20 searches. But there are still real issues.

## Critical Issues

### 1. "DEMO DATA" IS NOT REAL DATA — Severity: HIGH
Every search says "Using demo data (N items) — live scrapers unavailable". The user is getting fake results. This is better than nothing, but the tool is still not scraping any real marketplace. The message is transparent, which is good, but a user wanting to *actually shop* still can't use this.

**What to do:** This is an environment constraint (proxy blocks marketplace sites). BUT — the tool should make it crystal clear this is demo mode. Add a visible banner or badge on the UI saying "Demo Mode" so users aren't confused. Also, when in production with no proxy, it should seamlessly try real scrapers first.

### 2. SEARCH RELEVANCE IS MEDIOCRE — Severity: MEDIUM
- "blue jeans size 32" returns **18 results** including monitors, headphones, and garden furniture. The word "blue" matches too aggressively — "Blue Titanium" in an iPhone title is not "blue jeans".
- "running shoes size 10" returns 13 results including vacuum cleaners, monitors, and watches. The word-matching is too loose — any single word match counts.
- "4K monitor 27 inch" returns 8 results, which is OK, but includes items that are 32 inch.

**Root cause:** The demo scraper scores items by individual word matches. A single common word like "blue" or "black" scores +2.0 regardless of context. Need minimum relevance threshold and/or multi-word phrase matching.

### 3. FILTER CHECKBOXES DON'T UPDATE COUNTS — Severity: MEDIUM
When I uncheck "Amazon" in the marketplace filter, items disappear but the result count at the top doesn't update. It still says "18 results" even though I'm now seeing 12. Confusing.

## Major Issues

### 4. NO "CLEAR FILTERS" BUTTON — Severity: MEDIUM
If I check/uncheck a bunch of filters, there's no quick way to reset them all. Have to manually re-check each one.

### 5. RESULT CARDS DON'T SHOW ENOUGH INFO — Severity: MEDIUM
- No "condition" badge on most items (only shows when in raw_attributes)
- The attribute tags at the bottom are nice but tiny and hard to read
- No indication of whether the link goes to a real page or a demo URL

### 6. SORT RESETS WHEN CHANGING FILTERS — Severity: LOW
If I sort by "Price: Low to High" then uncheck a marketplace filter, the visual order appears to reset. Sorting and filtering should work together.

### 7. NO SEARCH SUGGESTIONS OR AUTOCOMPLETE — Severity: LOW
The search box gives no suggestions. For a tool that "automatically detects what you're asking for," it would be great to show suggestions as you type: "Did you mean: Nike Air Max?" or "Detected: brand=Nike, colour=black".

### 8. IMAGE LOADING FAILURES — Severity: LOW
The picsum.photos placeholder images sometimes fail to load (timeout or 404). The onerror fallback works but it makes the page look broken with lots of package icons.

## What's Good Now (Improvements Noticed)

- All 20 searches return results (up from 0/20)
- Brand, colour, condition, material, and size are all detected correctly
- The intent badges below the search bar are helpful — "Brand: dyson | Condition: refurbished"
- Sorting works (price low/high, name A-Z)
- Dynamic filters appear and actually work now
- The "Using demo data" message is honest and informative
- The dark theme UI is still clean and professional

## Summary

The tool went from **completely broken** to **functional demo**. The architecture is now proven end-to-end: search → parse intent → query scrapers (demo) → categorise → filter → display. The remaining issues are about quality: search relevance, UX polish, and eventually plugging in real scrapers.

**Priority fixes for iteration 2:**
1. Add a minimum relevance threshold to stop irrelevant results
2. Add a "Demo Mode" banner so users aren't confused
3. Fix filter count not updating when filtering
4. Add "Clear Filters" button
5. Improve result card info density
