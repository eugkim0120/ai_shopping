"""Tests for the web API endpoints."""

import pytest
from fastapi.testclient import TestClient

from ai_shopping.web.app import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_index_returns_html(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "AI Shopping" in resp.text


def test_search_empty_query_returns_empty(client):
    resp = client.get("/api/search?q=")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_marketplaces_endpoint(client):
    resp = client.get("/api/marketplaces")
    assert resp.status_code == 200
    data = resp.json()
    assert "marketplaces" in data
    assert "amazon" in data["marketplaces"]
    assert "ebay" in data["marketplaces"]
