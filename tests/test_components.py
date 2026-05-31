# -*- coding: utf-8 -*-
import importlib

COMPONENTS = [
    "components.hero",
    "components.about",
    "components.projects",
    "components.skills",
    "components.tech_stack",
    "components.articles",
    "components.playground",
    "components.contact",
]

def test_all_components_import():
    """All component modules should import without error."""
    for mod_name in COMPONENTS:
        mod = importlib.import_module(mod_name)
        assert mod is not None, f"Failed to import {mod_name}"

def test_all_components_have_render():
    """Each component should have a render_* function."""
    expected = {
        "components.hero": "render_hero",
        "components.about": "render_about",
        "components.projects": "render_projects",
        "components.skills": "render_skills",
        "components.tech_stack": "render_tech_stack",
        "components.articles": "render_articles",
        "components.playground": "render_playground",
        "components.contact": "render_contact",
    }
    for mod_name, func_name in expected.items():
        mod = importlib.import_module(mod_name)
        assert hasattr(mod, func_name), f"{mod_name} missing {func_name}"
        assert callable(getattr(mod, func_name)), f"{func_name} not callable"
