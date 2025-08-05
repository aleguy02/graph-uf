"""
Tests for non-API routes
"""

import pytest


def test_bad_route(client):
    response = client.get("/bad")
    assert "<h1>Oops! There's nothing to see here</h1>" in response.get_data(
        as_text=True
    )


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    headers = dict(response.headers)

    assert "<title>GraphUF</title>" in html
    assert headers["Content-Type"] == "text/html; charset=utf-8"
