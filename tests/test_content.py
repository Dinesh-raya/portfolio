# -*- coding: utf-8 -*-
import os
import glob

def test_content_directory_exists():
    """content/ directory should exist."""
    content_path = os.path.join(os.path.dirname(__file__), "..", "content")
    assert os.path.exists(content_path), "content/ directory not found"

def test_markdown_files_have_frontmatter():
    """All .md files should have valid frontmatter."""
    content_path = os.path.join(os.path.dirname(__file__), "..", "content")
    md_files = glob.glob(os.path.join(content_path, "*.md"))
    assert len(md_files) > 0, "No markdown files found in content/"
    for filepath in md_files:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        assert content.startswith("---"), f"{filepath}: missing frontmatter start"
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{filepath}: incomplete frontmatter"
        frontmatter = parts[1].strip()
        for field in ["title", "date", "category", "excerpt"]:
            assert f"{field}:" in frontmatter, f"{filepath}: missing {field} in frontmatter"

def test_load_articles_function():
    """load_articles should return list of article dicts."""
    from utils.helpers import load_articles
    articles = load_articles()
    assert isinstance(articles, list)
    assert len(articles) > 0, "No articles loaded"
    for art in articles:
        assert "title" in art
        assert "date" in art
        assert "category" in art
        assert "excerpt" in art
        assert "read_time" in art
        assert "content" in art
