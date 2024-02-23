import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_temperature():
    response = client.get("/temperature")
    assert response.status_code == 200
    assert "temperature_celsius" in response.json()


def test_check_rain():
    response = client.get("/rain")
    assert response.status_code == 200
    assert "will_it_rain" in response.json()
