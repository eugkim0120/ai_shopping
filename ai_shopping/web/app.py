"""FastAPI application — serves the web UI and API endpoints."""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ai_shopping.categorisation.engine import CategorisationEngine
from ai_shopping.scrapers.amazon import AmazonScraper
from ai_shopping.scrapers.ebay import EbayScraper
from ai_shopping.scrapers.facebook import FacebookMarketplaceScraper
from ai_shopping.scrapers.gumtree import GumtreeScraper
from ai_shopping.scrapers.registry import ScraperRegistry
from ai_shopping.scrapers.vinted import VintedScraper
from ai_shopping.search.detector import SearchDetector
from ai_shopping.search.orchestrator import SearchOrchestrator
from ai_shopping.web.api import router as api_router

WEB_DIR = Path(__file__).parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    registry = ScraperRegistry()
    registry.register(AmazonScraper())
    registry.register(EbayScraper())
    registry.register(GumtreeScraper())
    registry.register(FacebookMarketplaceScraper())
    registry.register(VintedScraper())

    detector = SearchDetector()
    categoriser = CategorisationEngine()
    orchestrator = SearchOrchestrator(registry, detector, categoriser)

    app.state.registry = registry
    app.state.orchestrator = orchestrator

    yield

    await registry.close_all()


app = FastAPI(title="AI Shopping", version="0.5.0", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=WEB_DIR / "static"), name="static")
app.include_router(api_router, prefix="/api")

templates = Jinja2Templates(directory=WEB_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "marketplaces": ["amazon", "ebay", "gumtree", "facebook_marketplace", "vinted"],
    })
