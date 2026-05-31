import importlib
import sys


def test_load_articles_nonexistent_dir():
    from utils.helpers import load_articles
    result = load_articles(content_dir="nonexistent_dir_xyz")
    assert result == []


def test_load_articles_bad_frontmatter():
    import tempfile, os
    tmp = tempfile.mkdtemp()
    bad_file = os.path.join(tmp, "bad.md")
    with open(bad_file, "w") as f:
        f.write("This is not frontmatter")

    from utils.helpers import load_articles
    articles = load_articles(content_dir=tmp)
    assert len(articles) == 0


def test_empty_projects_html():
    from components.hero import _projects_html
    html = _projects_html([])
    assert html == ""


def test_empty_timeline_html():
    from components.hero import _timeline_html
    html = _timeline_html([])
    assert "timeline" in html.lower()
