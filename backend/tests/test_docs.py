from fastapi.testclient import TestClient

from app.main import app


REDOC_JS_URL = "https://cdn.redoc.ly/redoc/v2.5.3/bundles/redoc.standalone.js"


def test_redoc_uses_pinned_official_standalone_bundle():
    response = TestClient(app).get("/redoc")

    assert response.status_code == 200
    assert f'<script src="{REDOC_JS_URL}">' in response.text
    assert "redoc@2" not in response.text


def test_openapi_json_remains_public():
    response = TestClient(app).get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Food Store API"
