# -*- coding: utf-8 -*-
import importlib
from unittest.mock import patch, MagicMock


def test_app_imports():
    """app.py should import without error (GitHub API mocked)."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = []
    with patch("utils.helpers.requests.get", return_value=mock_resp):
        import app as app_module
        assert app_module is not None
    # Clean up so subsequent runs don't use stale module
    import sys
    if "app" in sys.modules:
        del sys.modules["app"]

def test_all_imports_succeed():
    """All project modules should import without error."""
    modules = [
        "data.portfolio_data",
        "utils.helpers",
        "components.hero",
        "components.about",
        "components.projects",
        "components.skills",
        "components.tech_stack",
        "components.articles",
        "components.playground",
        "components.contact",
    ]
    for mod in modules:
        m = importlib.import_module(mod)
        assert m is not None, f"Failed to import {mod}"
