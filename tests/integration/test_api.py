import json
from unittest.mock import Mock
import pytest
from tracker.api import app, tv_adapter
from fastapi.testclient import TestClient

from tracker.query.model import Show, TVShowLength


@pytest.fixture(autouse=True)
def mock_tv_adapter():
    mock = Mock()
    app.dependency_overrides[tv_adapter] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


@pytest.fixture
def api_client():
    return TestClient(app)


def test_api__when_calling_healthz_endpoint__returns_ok(
    api_client,
):
    response = api_client.get("/api/healthz")
    assert response.status_code == 200
    assert response.json() == {"o": "k"}


def test_api__when_calling_version_endpoint__returns_version_in_tracker_init(
    api_client,
):
    from tracker import __version__

    response = api_client.get("/api/version")
    assert response.status_code == 200
    assert response.json() == {"version": __version__}


def test_api__when_calling_tv_search_endpoint_and_empty__returns_empty_results(
    api_client,
    mock_tv_adapter,
):
    mock_tv_adapter.search.return_value = []

    response = api_client.get("/api/tv/search", params={"query": "One Piece"})
    assert response.status_code == 200
    assert response.json() == {"results": []}


def test_api__when_calling_tv_search_endpoint_and_results_found__returns_results(
    api_client,
    mock_tv_adapter,
):
    mock_tv_adapter.search.return_value = [
        Show(
            name="One Piece",
            description="Goofy Pirate goes Brrrr",
            genres=["Action", "Adventure"],
            length=TVShowLength(seasons=1, episodes_per_season={1: 1317}),
            networks=["Funimation", "Crunchyroll"],
        )
    ]

    response = api_client.get("/api/tv/search", params={"query": "One Piece"})
    assert response.status_code == 200, response.text
    data = response.json()
    expected = {
        "results": [
            {
                "name": "One Piece",
                "description": "Goofy Pirate goes Brrrr",
                "genres": ["Action", "Adventure"],
                "length": {
                    "seasons": 1,
                    "episodes_per_season": {"1": 1317},
                    "episodes": 1317,
                },
                "networks": ["Funimation", "Crunchyroll"],
                "banner": None,
                "poster": None,
            }
        ]
    }
    assert data == expected, "Got: {}\nExpected: {}".format(data, expected)


def test_api__when_calling_tv_trending_endpoint_with_day_and_results_found__returns_results(
    api_client,
    mock_tv_adapter,
):
    mock_tv_adapter.trending.return_value = [
        Show(
            name="One Piece",
            description="Goofy Pirate goes Brrrr",
            genres=["Action", "Adventure"],
            length=TVShowLength(seasons=1, episodes_per_season={1: 1317}),
            networks=["Funimation", "Crunchyroll"],
        )
    ]

    response = api_client.get("/api/tv/trending/day")
    assert response.status_code == 200
    data = response.json()
    expected = {
        "results": [
            {
                "name": "One Piece",
                "description": "Goofy Pirate goes Brrrr",
                "genres": ["Action", "Adventure"],
                "length": {
                    "seasons": 1,
                    "episodes_per_season": {"1": 1317},
                    "episodes": 1317,
                },
                "networks": ["Funimation", "Crunchyroll"],
                "banner": None,
                "poster": None,
            }
        ]
    }
    assert data == expected, "Got: {}\nExpected: {}".format(data, expected)


def test_api__when_calling_tv_trending_endpoint_with_day_and_no_results_found__returns_no_results(
    api_client,
    mock_tv_adapter,
):
    mock_tv_adapter.trending.return_value = []

    response = api_client.get("/api/tv/trending/day")
    assert response.status_code == 200
    data = response.json()
    expected = {"results": []}
    assert data == expected, "Got: {}\nExpected: {}".format(data, expected)


def test_api__when_calling_tv_trending_endpoint_with_week_and_results_found__returns_results(
    api_client,
    mock_tv_adapter,
):
    mock_tv_adapter.trending.return_value = [
        Show(
            name="One Piece",
            description="Goofy Pirate goes Brrrr",
            genres=["Action", "Adventure"],
            length=TVShowLength(seasons=1, episodes_per_season={1: 1317}),
            networks=["Funimation", "Crunchyroll"],
        )
    ]

    response = api_client.get("/api/tv/trending/week")
    assert response.status_code == 200
    data = response.json()
    expected = {
        "results": [
            {
                "name": "One Piece",
                "description": "Goofy Pirate goes Brrrr",
                "genres": ["Action", "Adventure"],
                "length": {
                    "seasons": 1,
                    "episodes_per_season": {"1": 1317},
                    "episodes": 1317,
                },
                "networks": ["Funimation", "Crunchyroll"],
                "banner": None,
                "poster": None,
            }
        ]
    }
    assert data == expected, "Got: {}\nExpected: {}".format(data, expected)


def test_api__when_calling_tv_trending_endpoint_with_week_and_no_results_found__returns_no_results(
    api_client,
    mock_tv_adapter,
):
    mock_tv_adapter.trending.return_value = []

    response = api_client.get("/api/tv/trending/week")
    assert response.status_code == 200
    data = response.json()
    expected = {"results": []}
    assert data == expected, "Got: {}\nExpected: {}".format(data, expected)
