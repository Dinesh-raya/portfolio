import pytest
from utils.helpers import load_articles


def test_at_least_10_articles():
    articles = load_articles()
    assert len(articles) >= 10, f"Expected >=10 articles, got {len(articles)}"


def test_articles_have_required_fields():
    articles = load_articles()
    for a in articles:
        assert a["title"], f"Article missing title: {a}"
        assert a["category"], f"Article missing category: {a}"
        assert a["excerpt"], f"Article missing excerpt: {a}"
        assert a["content"], f"Article missing content: {a}"
        assert a["date"], f"Article missing date: {a}"


def test_articles_categories_are_valid():
    articles = load_articles()
    valid = {"Artificial Intelligence", "Software Engineering", "Python & Software Design"}
    for a in articles:
        assert a["category"] in valid, f"Invalid category '{a['category']}' in '{a['title']}'"


def test_articles_are_sorted_by_date():
    articles = load_articles()
    dates = [a["date"] for a in articles]
    assert dates == sorted(dates, reverse=True), "Articles not sorted newest-first"
