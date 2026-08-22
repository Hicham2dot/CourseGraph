"""Fixtures partagées pour pytest."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from coursegraph.api.main import app


@pytest.fixture
def client() -> TestClient:
    """Client de test FastAPI synchrone."""
    return TestClient(app)


@pytest.fixture
def sample_course_name() -> str:
    """Nom de cours utilisé dans les tests."""
    return "test_course"
