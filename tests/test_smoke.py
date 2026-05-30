# -*- coding: utf-8 -*-
import importlib

def test_app_imports():
    """app.py should import without error."""
    import app
    assert app is not None

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
        "components.experience",
        "components.articles",
        "components.playground",
        "components.contact",
    ]
    for mod in modules:
        m = importlib.import_module(mod)
        assert m is not None, f"Failed to import {mod}"
