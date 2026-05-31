---
title: "Data Quality Automation with Python"
date: "2026-04-25"
category: "Software Engineering"
excerpt: "A practical guide to building automated data quality checks using Great Expectations-style patterns with plain Python and Pandas."
---

# Data Quality Automation with Python

Data quality isn't optional — it's the foundation every downstream decision rests on. Automating quality checks catches problems before they propagate, saves debugging time, and builds trust in your data pipelines.

## Why Automate Data Quality?

Manual data validation is slow, inconsistent, and doesn't scale. Automated checks:

- Run on every pipeline execution
- Catch regressions immediately
- Produce consistent, comparable reports
- Free up engineers for higher-value work

## Building a Validation Framework

You don't need a heavy framework. A validation pipeline can be built with plain Python classes:

```python
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Check:
    name: str
    func: Callable
    severity: str = "error"  # error, warning, info

class DataValidator:
    def __init__(self):
        self.checks = []

    def add_check(self, check: Check):
        self.checks.append(check)

    def run(self, df) -> list[dict]:
        results = []
        for check in self.checks:
            try:
                passed = check.func(df)
                results.append({
                    "check": check.name,
                    "passed": passed,
                    "severity": check.severity,
                })
            except Exception as e:
                results.append({
                    "check": check.name,
                    "passed": False,
                    "severity": check.severity,
                    "error": str(e),
                })
        return results
```

## Essential Quality Checks

Here are the checks I include in every pipeline:

### Completeness Checks

Ensure critical columns have no missing values:

```python
def check_completeness(df, columns: list[str], threshold: float = 0.95):
    for col in columns:
        null_ratio = df[col].isnull().mean()
        if null_ratio > (1 - threshold):
            return False
    return True
```

### Uniqueness Checks

Verify primary key columns contain no duplicates:

```python
def check_uniqueness(df, column: str) -> bool:
    return df[column].is_unique
```

### Range Checks

Validate numeric columns fall within expected bounds:

```python
def check_range(df, column: str, min_val=None, max_val=None) -> bool:
    if min_val is not None and df[column].min() < min_val:
        return False
    if max_val is not None and df[column].max() > max_val:
        return False
    return True
```

### Schema Checks

Confirm column names and types match expectations:

```python
def check_schema(df, expected_schema: dict[str, str]) -> bool:
    for col, dtype in expected_schema.items():
        if col not in df.columns:
            return False
        if str(df[col].dtype) != dtype:
            return False
    return True
```

## Reporting Results

Format validation results into a clear report:

```python
def generate_report(results: list[dict]) -> str:
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    report = f"# Data Quality Report\n\n"
    report += f"**{passed}/{total} checks passed**\n\n"
    report += "| Check | Status | Severity |\n"
    report += "|-------|--------|----------|\n"
    for r in results:
        status = "✅" if r["passed"] else "❌"
        report += f"| {r['check']} | {status} | {r['severity']} |\n"
    return report
```

## Integrating into Pipelines

The validator runs at the ingestion stage of every data pipeline:

```
Source → Extract → Validate → Transform → Validate → Load
```

This two-stage validation catches issues early and prevents bad data from reaching downstream consumers.

## Key Takeaways

1. Start with the five essential checks: completeness, uniqueness, range, schema, and freshness
2. Build checks incrementally as you discover data issues
3. Make validation reports accessible to non-technical stakeholders
4. Fail pipelines on critical check failures, warn on non-critical ones
5. Version your validation rules alongside your pipeline code

Automated data quality transforms trust from a hope into a guarantee. Every pipeline deserves it.
