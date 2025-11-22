"""Tests for datatools.fetch module.

These tests use monkeypatching to avoid real HTTP requests and
to keep the tests fast and deterministic.
"""

from typing import Any

import pytest

from datatoolsdemo import fetch_json


class DummyResponse:
    """Simple dummy response object used for mocking requests.get."""

    def __init__(
        self,
        json_data: dict[str, Any],
        status_code: int = 200,
    ) -> None:
        """Initialize class instance."""
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self) -> None:
        """Simulate raise_for_status behavior based on status code."""
        if self.status_code >= 400:
            msg = f"HTTP error {self.status_code}"
            raise Exception(msg)

    def json(self) -> dict[str, Any]:
        """Return the stored JSON data."""
        return self._json_data


def test_fetch_json_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that fetch_json returns parsed JSON on successful response."""

    def fake_get(url: str, timeout: int = 5) -> DummyResponse:  # type: ignore[override]
        assert url == "https://example.com/api"
        return DummyResponse({"message": "ok"}, status_code=200)

    # Patch requests.get in the datatools.fetch module
    monkeypatch.setattr("datatoolsdemo.fetch.requests.get", fake_get)

    result = fetch_json("https://example.com/api")
    assert result == {"message": "ok"}


def test_fetch_json_http_error(monkeypatch: pytest.MonkeyPatch) -> None:
    """Verify that fetch_json raises RuntimeError if the HTTP request fails."""

    def fake_get(url: str, timeout: int = 5) -> DummyResponse:  # type: ignore[override]
        return DummyResponse({"error": "broken"}, status_code=500)

    monkeypatch.setattr("datatoolsdemo.fetch.requests.get", fake_get)

    with pytest.raises(RuntimeError):
        fetch_json("https://example.com/api")


def test_fetch_json_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Verify that any unexpected exception from requests.get also results in a
    RuntimeError, keeping the public API consistent.
    """

    def fake_get(url: str, timeout: int = 5) -> Any:  # type: ignore[override]
        raise TimeoutError("Network down")

    monkeypatch.setattr("datatoolsdemo.fetch.requests.get", fake_get)

    with pytest.raises(RuntimeError):
        fetch_json("https://example.com/api")
