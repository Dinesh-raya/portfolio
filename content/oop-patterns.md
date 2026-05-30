---
title: "Practical OOP Design Patterns in Python"
date: "2026-03-10"
category: "Python & Software Design"
excerpt: "Learn how Singleton, Factory, and Strategy patterns make automation code modular, testable, and robust."
---

# Practical OOP Design Patterns in Python

Design patterns aren't just academic exercises. When applied judiciously, they solve real problems in automation, scripting, and application code. Here are three patterns I use regularly in production Python.

## The Singleton Pattern

Use when you need exactly one instance of a class throughout your application. Common use cases include configuration managers, database connection pools, and logging handlers.

```python
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """Load configuration from environment and files."""
        import os
        self.debug = os.getenv("DEBUG", "false").lower() == "true"
        self.db_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
        self.api_key = os.getenv("API_KEY", "")
```

Benefits:
- Single source of truth for configuration
- Lazy initialization on first access
- Thread-safe with proper locking if needed

Cautions:
- Makes testing harder (state persists between tests)
- Can hide dependencies
- Consider dependency injection as an alternative

## The Factory Pattern

Use when you need to create objects based on runtime conditions. This is especially useful for plugin systems, format handlers, and API client selection.

```python
class ScraperFactory:
    _scrapers = {}

    @classmethod
    def register(cls, source: str, scraper_class):
        cls._scrapers[source] = scraper_class

    @classmethod
    def create(cls, source: str):
        scraper_class = cls._scrapers.get(source)
        if not scraper_class:
            raise ValueError(f"Unknown source: {source}")
        return scraper_class()

# Registration
ScraperFactory.register("github", GitHubScraper)
ScraperFactory.register("linkedin", LinkedInScraper)

# Usage
scraper = ScraperFactory.create("github")
```

Benefits:
- Decouples creation logic from usage
- Easy to add new types without modifying existing code
- Centralizes configuration and initialization

## The Strategy Pattern

Use when you need interchangeable algorithms or behaviors. This pattern shines for export formats, validation rules, and pricing models.

```python
class DataExporter:
    def __init__(self, strategy):
        self.strategy = strategy

    def export(self, data):
        return self.strategy(data)

# Strategies as simple functions
def csv_strategy(data):
    import pandas as pd
    return pd.DataFrame(data).to_csv(index=False)

def json_strategy(data):
    import json
    return json.dumps(data, indent=2, default=str)

def markdown_strategy(data):
    headers = data[0].keys()
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    for row in data:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    return "\n".join(lines)

# Usage
exporter = DataExporter(csv_strategy)
print(exporter.export(records))
```

Benefits:
- Algorithms are first-class objects
- Easy to swap behaviors at runtime
- Each strategy is independently testable

## When to Use Patterns

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| Singleton | Global config, logging, connection pools | You need multiple instances or easy testing |
| Factory | Plugin systems, format handlers, conditional creation | Only 1-2 types that never change |
| Strategy | Export formats, validation rules, sorting algorithms | Algorithm rarely changes |

## Key Insight

Patterns should emerge from problems, not be applied preemptively. Start with the simplest solution that works. When complexity demands it, refactor to patterns. Premature abstraction is worse than no abstraction.

The best code is code that clearly communicates intent. If a pattern makes your code harder to read, it's the wrong pattern for that situation.
