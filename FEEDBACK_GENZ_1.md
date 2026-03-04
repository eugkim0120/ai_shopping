# Gen Z Customer Feedback — Iteration 1
**Rating**: 3/10 — "this app is giving mid tbh"

## The Good
- Sony headphones search is actually fire (5 results, all relevant)
- AirPods Pro found immediately
- Gaming keyboard RGB works and prices are right
- Camping tent search nailed it

## The Bad (12 of 20 searches FAILED)

### No Data for Popular Gen Z Products
- "Stanley cup tumbler" — 0 results. EVERYONE has a Stanley cup rn
- "Dyson Airwrap" — 0 results. It's literally the most wanted hair tool
- "lululemon leggings" — 0 results. This is basic shopping
- "cheap protein powder" — 0 results. Gym bro essentials

### Search Doesn't Understand Natural Language
- "secondhand designer wallet" — 0 results. The word "secondhand" isn't
  treated as a condition synonym for "used". And "designer" means premium brands
- "aesthetic desk lamp" — 0 results. There ARE desk lamps in the demo data
  but the word "aesthetic" breaks matching
- "vintage Casio watch gold" — 0 results. The word "vintage" breaks it.
  There ARE gold Casio watches in the data!

### Marketplace-specific Searches Broken
- "vinted leather jacket" — 0 results. "vinted" is parsed as a marketplace
  filter, leaving "leather jacket" as the query, but there are no leather
  jackets in web data
- "running shoes under £80" — 0 results. No running shoes in web data at all

### Wrong Results
- "Samsung Galaxy Buds" — returns Galaxy Fit and Galaxy Tab, NOT Galaxy Buds!
  It's matching "samsung" and "galaxy" but ignoring "buds"
- "electric scooter budget" — returns £599-£699 scooters. That's not budget!
  The word "budget" should filter to cheaper options

### Missing from Data Catalogue
- "Nike dunks" — no Dunks in the web data at all
- "yoga mat thick" — only in demo data, not web data
- "refurbished MacBook" — no MacBooks at all

## What Needs Fixing
1. Add more Gen Z products to the catalogue (Stanley, Dyson Airwrap, lululemon, etc.)
2. Treat "secondhand" as synonym for "used"
3. Treat "vintage" as synonym for "used"
4. Ignore filler/adjective words like "aesthetic", "cheap", "budget"
5. Fix Galaxy Buds matching — "buds" should match "earbuds" not "tabs"
6. "budget" and "cheap" should prefer lower-priced items, not just be ignored
