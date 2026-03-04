# Test Report

## v0.2.0 — 2026-03-04

**23 passed, 0 failed** (1.72s)

### Categorisation Engine (6 tests)
- test_extracts_price_category PASSED
- test_extracts_colour_from_title PASSED
- test_extracts_size_spec_from_title PASSED
- test_extracts_brand_from_attributes PASSED
- test_get_filter_options_returns_sorted_values PASSED
- test_empty_items_returns_empty_categories PASSED

### Scraper Registry (4 tests)
- test_register_and_get PASSED
- test_get_returns_none_for_unknown PASSED
- test_all_returns_registered_scrapers PASSED
- test_fake_scraper_search PASSED

### Search Detector (10 tests)
- test_basic_query PASSED
- test_extracts_max_price PASSED
- test_extracts_min_price PASSED
- test_extracts_price_range PASSED
- test_extracts_colour PASSED
- test_extracts_condition PASSED
- test_extracts_marketplace PASSED
- test_extracts_facebook_alias PASSED
- test_complex_query PASSED
- test_no_filters_detected PASSED

### Web API (3 tests)
- test_index_returns_html PASSED
- test_search_empty_query_returns_empty PASSED
- test_marketplaces_endpoint PASSED
