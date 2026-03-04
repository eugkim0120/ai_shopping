# Customer Feedback — Iteration 4 (Post-Synonym & Brand Fix)

**Date**: 2026-03-04
**Tester**: Critical Customer
**Rating**: 7.5/10 — SOLID TOOL WITH REMAINING POLISH NEEDED

---

## What Improved (from Iteration 3)

- **Synonym matching works brilliantly!** "baby pushchair stroller" now returns 6 results — it found pushchairs via synonym expansion. This is exactly what a real shopping tool needs.
- **Brand filtering is now strict**: "noise cancelling headphones Sony" returns only Sony products. Down from 10 mixed results to 7 Sony-only results.
- **20/20 searches return results** — zero failures, up from 19/20.
- **Marketplace chips now wired up** to the API — users can actually deselect marketplaces.

## Remaining Issues

### 1. "wireless earbuds noise cancelling" still returns 16 results — too broad
This 4-word query still matches too liberally. Over-ear headphones like "Bose 700 Noise Cancelling Headphones" appear when I searched specifically for earbuds. The type distinction (earbuds vs headphones) needs to be respected as a hard filter when "earbuds" is in the query.

### 2. No "type" aware filtering
The system treats "earbuds", "headphones", "speaker" all as generic words. It should understand that if I search for "earbuds", I don't want over-ear headphones. The `type` attribute in the data exists but isn't used for filtering — only for display.

### 3. Results could be grouped/highlighted by marketplace
When I see 7 results for "mens leather wallet", I have to scan each card to see which marketplace. A visual grouping or marketplace colour-coding would help comparison shopping.

### 4. No "data freshness" indicator
Prices are from web searches done today, but the user has no way to know when data was collected. Adding a "Prices as of March 2026" note would build trust.

### 5. Sort "Relevance" still doesn't work properly
The default sort is price ascending (cheapest first). When I select "Relevance" from the dropdown, nothing changes because the server always returns items sorted by price. Relevance sort should use the scoring from the search algorithm.

### 6. Search input doesn't show what was parsed
If I type "espresso machine under £200", the intent badges show "Max: £200" but the search input still shows my raw query. Would be nice to show what the system understood in a more prominent way.

---

## Summary

This is now a genuinely useful multi-marketplace comparison tool. The synonym matching, brand filtering, and real web data make it feel like a real product. The main areas for final polish: tighter type-aware filtering (earbuds vs headphones), relevance-based sort, and better visual marketplace differentiation. The fundamentals are solid — 20/20 searches work, all return real products at real prices across 5 marketplaces.
