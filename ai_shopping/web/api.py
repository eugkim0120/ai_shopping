"""API endpoints for search and marketplace data."""

from dataclasses import asdict

from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/search")
async def search(request: Request, q: str = ""):
    if not q.strip():
        return {"items": [], "filter_options": {}, "total": 0, "errors": []}

    orchestrator = request.app.state.orchestrator
    result = await orchestrator.search(q)

    items_data = []
    for item in result["items"]:
        item_dict = asdict(item)
        items_data.append(item_dict)

    return {
        "items": items_data,
        "filter_options": result["filter_options"],
        "total": result["total"],
        "errors": result["errors"],
        "query": result["intent"].query,
        "parsed": {
            "min_price": result["intent"].min_price,
            "max_price": result["intent"].max_price,
            "colour": result["intent"].colour,
            "condition": result["intent"].condition,
            "marketplaces": result["intent"].marketplaces,
        },
    }


@router.get("/marketplaces")
async def list_marketplaces(request: Request):
    registry = request.app.state.registry
    return {"marketplaces": registry.names()}
