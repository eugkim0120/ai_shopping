"""End-to-end test: searches 20 NEW everyday items through the API and reports results."""

import asyncio
import json
import time
from datetime import datetime

import httpx

ITEMS_TO_SEARCH = [
    "bluetooth speaker portable",
    "robot vacuum cleaner",
    "mechanical keyboard",
    "mens leather wallet",
    "fitness tracker smartwatch",
    "wireless earbuds noise cancelling",
    "gaming mouse wireless",
    "electric scooter adult",
    "standing desk electric",
    "instant camera Instax",
    "waterproof hiking boots size 10",
    "espresso machine under £200",
    "iPad tablet",
    "power bank 20000mAh",
    "baby pushchair stroller",
    "weighted blanket 8kg",
    "resistance bands set",
    "cast iron skillet Lodge",
    "noise cancelling headphones Sony",
    "camping tent 2 person",
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
                {"title": i["title"][:80], "price": i["price"], "marketplace": i["marketplace"]}
                for i in (data.get("items") or [])[:5]
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


async def main():
    base_url = "http://127.0.0.1:8000"
    report = {
        "timestamp": datetime.now().isoformat(),
        "base_url": base_url,
        "results": [],
        "summary": {},
    }

    async with httpx.AsyncClient(base_url=base_url) as client:
        print(f"\n=== Testing {len(ITEMS_TO_SEARCH)} item searches (v2 — web-sourced data) ===\n")

        for i, query in enumerate(ITEMS_TO_SEARCH, 1):
            result = await test_search(client, query)
            report["results"].append(result)

            status = "OK" if result["success"] else "FAIL"
            total = result.get("total", "?")
            elapsed = result["elapsed_s"]
            errors = len(result.get("errors", []))

            print(f"  [{i:2d}/20] {status} | {elapsed:5.1f}s | {total:3} results | {errors} errors | {query}")

            if result.get("items_sample"):
                for s in result["items_sample"][:3]:
                    print(f"           -> {s['price']:>10} | {s['marketplace']:>12} | {s['title'][:60]}")

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
                if pf.get("brand"):
                    parts.append(f"brand={pf['brand']}")
                if pf.get("material"):
                    parts.append(f"material={pf['material']}")
                if pf.get("size"):
                    parts.append(f"size={pf['size']}")
                if parts:
                    print(f"           Parsed: {' | '.join(parts)}")

    # Summary
    successes = [r for r in report["results"] if r["success"]]
    failures = [r for r in report["results"] if not r["success"]]
    zero_results = [r for r in successes if r.get("total", 0) == 0]
    has_results = [r for r in successes if r.get("total", 0) > 0]
    times = [r["elapsed_s"] for r in report["results"]]

    report["summary"] = {
        "total_searches": len(ITEMS_TO_SEARCH),
        "api_successes": len(successes),
        "api_failures": len(failures),
        "zero_result_searches": len(zero_results),
        "searches_with_results": len(has_results),
        "avg_response_time_s": round(sum(times) / len(times), 2) if times else 0,
        "max_response_time_s": round(max(times), 2) if times else 0,
    }

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for k, v in report["summary"].items():
        print(f"  {k}: {v}")

    with open("test_e2e_report_v2.json", "w") as f:
        json.dump(report, f, indent=2, default=str)
    print("\nFull report written to test_e2e_report_v2.json")


if __name__ == "__main__":
    asyncio.run(main())
