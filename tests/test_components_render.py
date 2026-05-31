from data.portfolio_data import PORTFOLIO_DATA
from components.hero import (
    _skill_bars_html,
    _projects_html,
    _tech_grid_html,
    _timeline_html,
    _articles_html,
    _radar_chart,
    _github_repos_html,
)


def test_skill_bars_html_returns_html():
    skills = PORTFOLIO_DATA["skills"]
    html = _skill_bars_html(skills["radar"]["metrics"], skills["radar"]["values"])
    assert "skill-progress-fill" in html
    assert "<div" in html
    assert "95%" in html


def test_projects_html_returns_html():
    html = _projects_html(PORTFOLIO_DATA["projects"])
    assert len(html) > 50
    assert "card" in html.lower() or "project" in html.lower()


def test_tech_grid_html_returns_html():
    items = [{"name": "Python", "icon_svg": "python"}]
    html = _tech_grid_html(items)
    assert "Python" in html


def test_timeline_html_returns_html():
    timeline_data = [
        {"period": "2024", "title": "Job", "subtitle": "Co", "description": "Worked on X"}
    ]
    html = _timeline_html(timeline_data)
    assert "2024" in html
    assert "timeline" in html.lower()


def test_timeline_html_empty():
    html = _timeline_html([])
    assert "timeline" in html.lower()


def test_articles_html_returns_html():
    articles = [
        {"title": "Test Article", "category": "AI", "date": "2026-01-01",
         "excerpt": "Some excerpt", "read_time": "5 min"}
    ]
    html = _articles_html(articles)
    assert "Test Article" in html
    assert "2026-01-01" in html


def test_articles_html_empty():
    html = _articles_html([])
    assert "Articles Coming Soon" in html or "coming" in html.lower()


def test_radar_chart_returns_figure():
    skills = PORTFOLIO_DATA["skills"]
    fig = _radar_chart(skills, "dark")
    assert fig is not None


def test_github_repos_html_returns_html():
    repos = [{"name": "test-repo", "description": "A test repo",
              "html_url": "https://github.com/test/test-repo",
              "stargazers_count": 5, "language": "Python"}]
    html = _github_repos_html(repos)
    assert "test-repo" in html
