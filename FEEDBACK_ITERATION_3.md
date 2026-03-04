# Customer Feedback — Iteration 3 (Web-Sourced Real Data)

**Date**: 2026-03-04
**Tester**: Critical Customer
**Rating**: 6.5/10 — REAL DATA BUT ROUGH EDGES

---

## What Improved (from Iteration 2)

- Products are now REAL — actual JBL Flip 7 at £129.99, Sony WH-1000XM6 at £379, etc.
- Prices reflect genuine UK marketplace pricing from Amazon, eBay, Gumtree, Vinted
- Product URLs actually link to real marketplace search pages
- 19 out of 20 searches return results — huge improvement
- Multi-marketplace comparison works: same item at different prices across Amazon/eBay/Gumtree
- Intent parsing detects brand, price, material, size correctly (e.g. "espresso machine under £200" filters max price)

## Critical Issues

### 1. "baby pushchair stroller" returns ZERO results (5 marketplaces, 0 hits)
I know you have pushchairs in the data! The query "baby pushchair stroller" matches nothing because the scoring requires 60% of meaningful words to match. "baby" doesn't appear in most pushchair titles. The tool should handle synonym matching — "stroller" = "pushchair" = "pram" = "buggy". This is a showstopper for parents looking for baby products.

### 2. "wireless earbuds noise cancelling" returns 16 results — way too many
This includes earbuds, over-ear headphones, AND things like "Bose 700 Noise Cancelling Headphones" which are NOT earbuds. The query is 4 words so MIN_MATCH_RATIO of 0.5 means matching only 2 of 4 words is enough. "noise cancelling" matches every ANC product regardless of form factor.

### 3. "noise cancelling headphones Sony" returns 10 results including non-Sony products
I searched specifically for Sony but got Anker, Bose, and non-headphone products (earbuds). The brand filter should be much more aggressive — if I say "Sony", I want ONLY Sony products (or Sony first, others marked as alternatives).

## Major Issues

### 4. No product images
Every single product shows a placeholder box icon. The picsum.photos random images are generic — they're landscapes and objects that have nothing to do with the products. This makes the shopping experience look fake and unfinished.

### 5. No product links work properly
URLs like `https://www.amazon.co.uk/s?k=JBL+Flip+7` just go to an Amazon search page, not the actual product listing. A real shopping tool should link directly to the product. These are search URLs, not product URLs.

### 6. "power bank 20000mAh" returns 5000mAh products
The query specifically asks for 20000mAh but the Anker Nano 5000mAh shows up. Numeric specifications should be treated as hard filters, not fuzzy matches.

## Minor Issues

### 7. No indication that data is web-sourced vs live
The banner says "Web-Sourced Data" but there's no per-item provenance — when was this data collected? Are prices current? Users need to know prices may be stale.

### 8. Filter panel shows too many categories
For "bluetooth speaker", the filter panel shows connectivity, capacity, storage — these are attribute leak from other product types that matched weakly. Filters should only show categories relevant to the actual results displayed.

### 9. Sort "Relevance" doesn't actually sort by relevance
Items are sorted by price (lowest first) regardless of the sort dropdown. The server sorts by price as default, but when I select "Relevance" it should show the most relevant items first.

### 10. Marketplace chips in header are decorative
Clicking marketplace chips doesn't actually filter the API request. They're checkboxes that do nothing server-side. Either wire them up or remove them.

---

## Summary

The tool has made a massive leap from fake demo data to real products with real prices. The core multi-marketplace comparison is genuinely useful — I can see the same Logitech G305 mouse at different prices across Amazon and eBay. But the search relevance is still too loose (16 results for earbuds query), synonym handling is missing (pushchair/stroller gap), and the brand filter needs to be a hard constraint. The UI also desperately needs real product images and working product links.
