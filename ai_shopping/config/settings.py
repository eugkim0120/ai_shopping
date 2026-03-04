"""Application settings — super configurable via environment or config file."""

from dataclasses import dataclass, field


@dataclass
class ScraperConfig:
    enabled: bool = True
    timeout: float = 30.0
    max_results: int = 50
    user_agent: str = "AI-Shopping/0.1"
    custom_headers: dict[str, str] = field(default_factory=dict)


@dataclass
class Settings:
    """Top-level application settings."""

    scrapers: dict[str, ScraperConfig] = field(default_factory=lambda: {
        "amazon": ScraperConfig(),
        "ebay": ScraperConfig(),
        "gumtree": ScraperConfig(),
        "facebook_marketplace": ScraperConfig(),
        "vinted": ScraperConfig(),
    })
    web_host: str = "0.0.0.0"
    web_port: int = 8000
    debug: bool = False

    def get_scraper_config(self, name: str) -> ScraperConfig:
        return self.scrapers.get(name, ScraperConfig())
