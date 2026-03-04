"""End-to-end test: searches 20 everyday items through the API and reports results."""

import asyncio
import json
import sys
import time
from datetime import datetime

import httpx

ITEMS_TO_SEARCH = [
    "wireless headphones",
    "iPhone 15 Pro Max",
    "running shoes size 10",
    "black winter jacket under £80",
    "Samsung Galaxy S24 used",
    "coffee machine",
    "yoga mat",
    "kids bicycle",
    "Nintendo Switch OLED",
    "desk lamp LED",
    "protein powder chocolate",
    "women's handbag leather",
    "4K monitor 27 inch",
    "air fryer",
    "garden furniture set",
    "electric toothbrush",
    "blue jeans size 32",
    "Dyson vacuum cleaner refurbished",
    "PlayStation 5 controller",
    "gold watch under £200 on ebay",
]


async def test_search(client: httpx.AsyncClient, query: str) -> dict:
    start = time.monotonic()
    try:
        resp = await client.get("/api/search", params={"q": query}, timeout=60.0)
        elapsed = time.monotonic() - start
        data = resp.json()
        return {
            "query": query,
            "status": resp.status_code,
            "total": data.get("total", 0),
            "errors": data.get("errors", []),
            "parsed_query": data.get("query", ""),
            "parsed_filters": data.get("parsed", {}),
            "items_sample": [
                {"title": i["title"][:60], "price": i["price"], "marketplace": i["marketplace"]}
                for i in (data.get("items") or [])[:3]
            ],
            "filter_options": {k: len(v) for k, v in (data.get("filter_options") or {}).items()},
            "elapsed_s": round(elapsed, 2),
            "success": True,
        }
    except Exception as e:
        elapsed = time.monotonic() - start
        return {
            "query": query,
            "success": False,
            "error": str(e),
            "elapsed_s": round(elapsed, 2),
        }


async def test_marketplaces(client: httpx.AsyncClient) -> dict:
    resp = await client.get("/api/marketplaces")
    return resp.json()


async def test_index(client: httpx.AsyncClient) -> dict:
    resp = await client.get("/")
    return {"status": resp.status_code, "has_content": len(resp.text) > 100}


async def main():
    base_url = "http://127.0.0.1:8000"
    report = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "results": [],
        "summary": {},
    }

    async with httpx.AsyncClient(base_url=base_url) as client:
        # Test index page
        print("=== Testing index page ===")
        idx = await test_index(client)
        print(f"  Index: status={idx['status']}, has_content={idx['has_content']}")

        # Test marketplaces
        print("\n=== Testing /api/marketplaces ===")
        mp = await test_marketplaces(client)
        print(f"  Marketplaces: {mp.get('marketplaces', [])}")

        # Test 20 searches
        print(f"\n=== Testing {len(ITEMS_TO_SEARCH)} item searches ===\n")

        for i, query in enumerate(ITEMS_TO_SEARCH, 1):
            result = await test_search(client, query)
            report["results"].append(result)

            status = "OK" if result["success"] else "FAIL"
            total = result.get("total", "?")
            elapsed = result["elapsed_s"]
            errors = len(result.get("errors", []))

            print(f"  [{i:2d}/20] {status} | {elapsed:5.1f}s | {total:3} results | {errors} errors | {query}")

            if result.get("errors"):
                for err in result["errors"][:2]:
                    print(f"          ^ {err[:80]}")

            if result.get("parsed_filters"):
                pf = result["parsed_filters"]
                parts = []
                if pf.get("min_price") is not None:
                    parts.append(f"min=£{pf['min_price']}")
                if pf.get("max_price") is not None:
                    parts.append(f"max=£{pf['max_price']}")
                if pf.get("colour"):
                    parts.append(f"colour={pf['colour']}")
                if pf.get("condition"):
                    parts.append(f"cond={pf['condition']}")
                if pf.get("marketplaces"):
                    parts.append(f"from={','.join(pf['marketplaces'])}")
                if parts:
                    print(f"          Parsed: {' | '.join(parts)}")

    # Summary
    successes = [r for r in report["results"] if r["success"]]
    failures = [r for r in report["results"] if not r["success"]]
    zero_results = [r for r in successes if r.get("total", 0) == 0]
    has_results = [r for r in successes if r.get("total", 0) > 0]
    times = [r["elapsed_s"] for r in report["results"]]
    all_errors = []
    for r in successes:
        all_errors.extend(r.get("errors", []))

    report["summary"] = {
        "total_searches": len(ITEMS_TO_SEARCH),
        "api_successes": len(successes),
        "api_failures": len(failures),
        "zero_result_searches": len(zero_results),
        "searches_with_results": len(has_results),
        "total_scraper_errors": len(all_errors),
        "avg_response_time_s": round(sum(times) / len(times), 2) if times else 0,
        "max_response_time_s": round(max(times), 2) if times else 0,
        "min_response_time_s": round(min(times), 2) if times else 0,
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for k, v in report["summary"].items():
        print(f"  {k}: {v}")

    # Write full report
    with open("test_e2e_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("\nFull report written to test_e2e_report.json")


if __name__ == "__main__":
    asyncio.run(main())
