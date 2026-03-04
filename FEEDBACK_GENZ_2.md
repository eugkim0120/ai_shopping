# Gen Z Customer Feedback — Iteration 2

**Date:** 2026-03-04
**Rating:** 7/10 (up from 3/10)

## Test Results: 20/20 searches returned results

Major improvement from 8/20 to 20/20. The filler word filtering, expanded synonyms,
condition aliases, and new catalogue products made a big difference.

## What's Working Well

1. **Brand + product searches** — "AirPods Pro", "Samsung Galaxy Buds", "Dyson Airwrap",
   "lululemon leggings" all return correct, relevant results.
2. **Slang/filler handling** — "aesthetic desk lamp", "cheap protein powder",
   "iPad Air for uni" all work now. Words like "aesthetic", "cheap", "uni" don't break matching.
3. **Condition recognition** — "secondhand designer wallet", "refurbished MacBook",
   "vintage Casio watch gold" all correctly interpret the condition.
4. **Price filter** — "running shoes under £80" correctly returns only items ≤£80.
5. **Budget ranking** — "cheap protein powder" ranks £14.99 and £18.99 items above £49.99.
6. **Synonym matching** — "dunks" maps to trainers/sneakers, "macbook" maps to laptop,
   "tumbler" maps to cup/flask.

## Remaining Issues

### 1. Budget intent ignores product category (Medium)
"electric scooter budget" returns £599 and £699 scooters ranked equally with £249.99.
The budget bonus uses absolute thresholds (£50/£100) which are meaningless for
high-ticket categories. A £250 scooter IS budget; a £599 one is not.

**Suggestion:** Use relative pricing — boost items cheaper than the median price
in the result set rather than hard-coding absolute thresholds.

### 2. Thin catalogue for some searches (Medium)
- "secondhand designer wallet" — only 1 result
- "Bose speaker portable" — only 1 result
- "running shoes under £80" — only 2 results

Real Gen Z users expect 10+ results per search. The catalogue needs more depth
in these categories.

### 3. Result ordering could be smarter (Low)
"electric scooter budget" — Xiaomi Pro Max (£599) and Segway (£699) rank at top
despite the user explicitly wanting budget options. The cheaper options should rank first.

### 4. No marketplace preference for "vinted" keyword (Low)
"vinted leather jacket" returns results from vinted, which is correct, but the
keyword "vinted" is treated as a query term rather than a marketplace filter.
The detector should recognise "vinted" as a marketplace name.

## Scores by Query

| # | Query | Results | Quality | Notes |
|---|-------|---------|---------|-------|
| 1 | AirPods Pro | 2 | Good | Correct AirPods + alternative earbuds |
| 2 | Stanley cup tumbler | 3 | Good | Correct Stanley tumblers |
| 3 | Dyson Airwrap | 4 | Good | Correct Dyson products |
| 4 | lululemon leggings | 3 | Good | Correct brand + product |
| 5 | white Nike dunks size 10 | 5 | Good | Panda Dunks ranked first |
| 6 | gaming keyboard RGB | 3 | Good | Relevant keyboards |
| 7 | iPad Air for uni | 2 | Good | "uni" ignored correctly |
| 8 | secondhand designer wallet | 1 | Fair | Only 1 result, thin catalogue |
| 9 | cheap protein powder | 4 | Good | Cheapest ranked first |
| 10 | Sony headphones noise cancelling | 5 | Good | Correct Sony headphones |
| 11 | aesthetic desk lamp | 3 | Good | "aesthetic" ignored correctly |
| 12 | vintage Casio watch gold | 3 | Good | Gold Casio ranked first |
| 13 | running shoes under £80 | 2 | Fair | Correct filter, thin catalogue |
| 14 | vinted leather jacket | 2 | Good | Correct vinted results |
| 15 | Samsung Galaxy Buds | 6 | Good | Galaxy Buds ranked first now |
| 16 | electric scooter budget | 4 | Fair | Budget items not ranked first |
| 17 | yoga mat thick | 2 | Good | Correct thick mats |
| 18 | Bose speaker portable | 1 | Fair | Only 1 result |
| 19 | refurbished MacBook | 4 | Good | Refurbished ranks well |
| 20 | camping tent 2 person | 4 | Good | Relevant tents |
