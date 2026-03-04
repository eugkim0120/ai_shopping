"""API endpoints for search and marketplace data."""

from dataclasses import asdict

from fastapi import APIRouter, Request

from ai_shopping.utils import parse_price

router = APIRouter()


@router.get("/search")
async def search(request: Request, q: str = "", sort: str = "relevance", marketplaces: str = ""):
    if not q.strip():
        return {"items": [], "filter_options": {}, "total": 0, "errors": []}

    # Append marketplace filter to query if specified via URL param
    query = q
    if marketplaces:
        mp_list = [m.strip() for m in marketplaces.split(",") if m.strip()]
        if mp_list:
            query = f"{q} on {','.join(mp_list)}"

    orchestrator = request.app.state.orchestrator
    result = await orchestrator.search(query)

    items_data = [asdict(item) for item in result["items"]]

    # Apply sorting
    if sort == "price_asc":
        items_data.sort(key=lambda x: parse_price(x.get("price")) or float("inf"))
    elif sort == "price_desc":
        items_data.sort(key=lambda x: parse_price(x.get("price")) or 0, reverse=True)
    elif sort == "name_asc":
        items_data.sort(key=lambda x: x.get("title", "").lower())

    intent = result["intent"]
    return {
        "items": items_data,
        "filter_options": result["filter_options"],
        "total": result["total"],
        "errors": result["errors"],
        "query": intent.query,
        "parsed": {
            "min_price": intent.min_price,
            "max_price": intent.max_price,
            "colour": intent.colour,
            "brand": intent.brand,
            "condition": intent.condition,
            "material": intent.material,
            "size": intent.size,
            "marketplaces": intent.marketplaces,
        },
    }


@router.get("/marketplaces")
async def list_marketplaces(request: Request):
    registry = request.app.state.registry
    return {"marketplaces": registry.names()}
