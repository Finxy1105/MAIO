import os
import pytest
from fastapi.testclient import TestClient
from src.api import app


client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert "status" in body and "model_version" in body


def test_predict_shapes():
    payload = {
        "age": 0.02,
        "sex": -0.044,
        "bmi": 0.06,
        "bp": -0.03,
        "s1": -0.02,
        "s2": 0.03,
        "s3": -0.02,
        "s4": 0.02,
        "s5": 0.02,
        "s6": -0.001,
    }
    r = client.post("/predict", json=payload)
    # If model is missing locally (e.g., CI before train), allow 503
    assert r.status_code in (200, 503)
    if r.status_code == 200:
        body = r.json()
        assert isinstance(body.get("prediction"), (int, float))


