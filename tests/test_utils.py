# -*- coding: utf-8 -*-
from utils.helpers import get_tech_icon_url, error_boundary

def test_get_tech_icon_url_known():
    """Known tech names should return valid URLs."""
    url = get_tech_icon_url("python")
    assert url.startswith("https://")
    assert "python" in url.lower()

def test_get_tech_icon_url_unknown():
    """Unknown tech names should return fallback Python icon."""
    url = get_tech_icon_url("nonexistent")
    assert url.startswith("https://")
    assert "python" in url.lower()

def test_error_boundary_catches():
    """error_boundary should catch exceptions and not crash."""
    @error_boundary
    def failing():
        raise ValueError("test error")
    result = failing()
    assert result is None

def test_error_boundary_passes():
    """error_boundary should pass through successful calls."""
    @error_boundary
    def working():
        return 42
    result = working()
    assert result == 42
