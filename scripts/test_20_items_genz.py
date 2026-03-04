"""Gen Z customer search test — 20 new product searches."""

import asyncio
import json
import sys
import time

import httpx

BASE = "http://localhost:8000/api/search"

# 20 items Gen Z would actually search for
SEARCHES = [
    "AirPods Pro",
    "Stanley cup tumbler",
    "Dyson Airwrap",
    "lululemon leggings",
    "white Nike dunks size 10",
    "gaming keyboard RGB",
    "iPad Air for uni",
    "secondhand designer wallet",
    "cheap protein powder",
    "Sony headphones noise cancelling",
    "aesthetic desk lamp",
    "vintage Casio watch gold",
    "running shoes under £80",
    "vinted leather jacket",
    "Samsung Galaxy Buds",
    "electric scooter budget",
    "yoga mat thick",
    "Bose speaker portable",
    "refurbished MacBook",
    "camping tent 2 person",
]


async def run_tests():
    results = []
    async with httpx.AsyncClient(timeout=30) as client:
        for query in SEARCHES:
            start = time.time()
            resp = await client.get(BASE, params={"q": query})
            elapsed = time.time() - start
            data = resp.json()

            result = {
                "query": query,
                "total": data["total"],
                "time_ms": round(elapsed * 1000),
                "parsed": data.get("parsed", {}),
                "sample_titles": [
                    item["title"] for item in data["items"][:3]
                ],
                "sample_prices": [
                    item["price"] for item in data["items"][:3]
                ],
                "marketplaces": list({
                    item["marketplace"] for item in data["items"]
                }),
            }
            results.append(result)

            status = "OK" if data["total"] > 0 else "FAIL"
            print(
                f"[{status}] {query}: "
                f"{data['total']} results ({elapsed*1000:.0f}ms)"
            )
            if data["items"]:
                for item in data["items"][:2]:
                    print(f"      {item['title']} — {item['price']}")

    success = sum(1 for r in results if r["total"] > 0)
    print(f"\n{'='*60}")
    print(f"Results: {success}/{len(SEARCHES)} searches returned results")

    with open("test_genz_report.json", "w") as f:
        json.dump(results, f, indent=2)

    return success == len(SEARCHES)


if __name__ == "__main__":
    ok = asyncio.run(run_tests())
    sys.exit(0 if ok else 1)
