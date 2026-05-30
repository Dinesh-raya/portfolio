# -*- coding: utf-8 -*-
from data.portfolio_data import PORTFOLIO_DATA

def test_portfolio_data_has_required_keys():
    """PORTFOLIO_DATA should have all required top-level keys."""
    required = ["personal", "stats", "about", "skills", "projects", "tech_stack", "experience"]
    for key in required:
        assert key in PORTFOLIO_DATA, f"Missing key: {key}"

def test_personal_has_required_fields():
    """Personal data should have name, email, github."""
    personal = PORTFOLIO_DATA["personal"]
    for field in ["name", "email", "github", "role"]:
        assert field in personal, f"Missing personal field: {field}"

def test_stats_count():
    """Should have exactly 4 stats."""
    assert len(PORTFOLIO_DATA["stats"]) == 4

def test_stats_structure():
    """Each stat should have value, label, icon."""
    for stat in PORTFOLIO_DATA["stats"]:
        assert "value" in stat
        assert "label" in stat
        assert "icon" in stat

def test_projects_have_required_fields():
    """Each project should have title, description, tech."""
    for proj in PORTFOLIO_DATA["projects"]:
        assert "title" in proj
        assert "description" in proj
        assert "tech" in proj

def test_skills_have_categories():
    """Skills should have categories with title and items."""
    skills = PORTFOLIO_DATA["skills"]
    assert "categories" in skills, "Skills missing 'categories' key"
    assert len(skills["categories"]) > 0, "No skill categories"
    for cat in skills["categories"]:
        assert "title" in cat, f"Category missing title: {cat}"
        assert "items" in cat, f"Category missing items: {cat}"
        assert len(cat["items"]) > 0, f"Category '{cat.get('title')}' has no items"
