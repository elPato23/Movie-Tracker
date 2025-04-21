from unittest.mock import Mock
import pytest
from tracker.api import app, tv_adapter
from fastapi.testclient import TestClient


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
