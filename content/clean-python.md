---
title: "Writing Clean Python: Typing, Linting, and Testing"
date: "2026-03-25"
category: "Python & Software Design"
excerpt: "How type hints, automated linting, and a practical testing strategy transform Python code from throwaway scripts into maintainable systems."
---

# Writing Clean Python: Typing, Linting, and Testing

Python's flexibility is a double-edged sword. Without discipline, scripts become unmaintainable quickly. Three practices transform ad-hoc Python into production-grade code: static typing, automated linting, and thorough testing.

## Type Hints: Self-Documenting Contracts

Type hints catch entire categories of bugs at development time and serve as living documentation:

```python
from typing import Optional, List, Dict, Tuple

def process_transactions(
    transactions: List[Dict[str, float]],
    currency: str = "USD",
    min_amount: Optional[float] = None,
) -> Tuple[float, int]:
    """Process a list of transactions and return (total, count)."""
    filtered = transactions
    if min_amount is not None:
        filtered = [t for t in transactions if t.get("amount", 0) >= min_amount]
    total = sum(t.get("amount", 0) for t in filtered)
    return total, len(filtered)
```

Key benefits:
- IDEs provide accurate autocompletion and inline error detection
- Refactoring becomes safer — the type checker validates changes
- New team members understand function contracts instantly

Use `mypy` or `pyright` for static type checking:

```bash
mypy src/ --strict
```

## Linting: Automated Code Review

Linters enforce consistency and catch common mistakes automatically. I use `ruff` for speed and `pylint` for depth:

```toml
# pyproject.toml
[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "PL", "UP"]

[tool.ruff.per-file-ignores]
"tests/*" = ["PLR0913"]
```

Ruff runs in milliseconds and catches:
- Unused imports and variables
- Inconsistent naming conventions
- Complex functions that need refactoring
- Common security anti-patterns

## Testing Strategy

A practical testing pyramid for data applications:

```
     ╱╲
    ╱ E2E ╲
   ╱───────╲
  ╱ Integration ╲
 ╱────────────────╲
╱   Unit Tests     ╲
╱────────────────────╲
```

### Unit Tests

Test individual functions in isolation:

```python
def test_process_transactions_empty():
    assert process_transactions([]) == (0.0, 0)

def test_process_transactions_filter():
    txns = [{"amount": 10}, {"amount": 50}]
    total, count = process_transactions(txns, min_amount=20)
    assert total == 50.0
    assert count == 1
```

### Integration Tests

Test data pipeline stages together:

```python
def test_extract_transform_pipeline():
    raw = extract_source()
    cleaned = clean_data(raw)
    transformed = transform_features(cleaned)
    assert transformed.isnull().sum().sum() == 0
    assert len(transformed.columns) == expected_features
```

### Property-Based Testing

Test invariants that must always hold:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.floats(min_value=0, max_value=1e6)))
def test_aggregation_invariants(values):
    result = aggregate(values)
    assert result["count"] == len(values)
    assert result["sum"] >= 0
    assert result["mean"] == result["sum"] / result["count"]
```

## Continuous Integration

Automate all three practices in CI:

```yaml
# .github/workflows/ci.yml
jobs:
  quality:
    steps:
      - run: ruff check .
      - run: mypy src/ --strict
      - run: pytest tests/ --cov=src --cov-fail-under=80
```

This pipeline runs on every pull request, ensuring no degraded code reaches production.

## Practical Adoption Tips

1. **Start with linting**: Ruff is zero-config and catches the most issues
2. **Add types incrementally**: Type critical function signatures first
3. **Test the risky parts**: Focus tests on complex logic and edge cases
4. **Run checks in CI**: Never rely on developers running tools manually
5. **Keep it practical**: 100% test coverage is not the goal — meaningful coverage is

## Conclusion

Clean Python doesn't happen by accident. Type hints, linting, and testing form a feedback loop that catches errors early, documents intent, and makes codebases a joy to work in. Invest in these practices early — the compound interest is enormous.
