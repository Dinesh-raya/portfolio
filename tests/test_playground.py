from components.playground import _analyze_code


def test_analyze_code_clean():
    result = _analyze_code("x = 1\nprint(x)")
    assert "metrics" in result
    assert "issues" in result
    assert "score" in result
    assert result["metrics"]["lines"] == 2


def test_analyze_code_syntax_error():
    result = _analyze_code("x = ")
    assert "error" in result
    assert "Syntax" in result.get("error", "")


def test_analyze_code_empty():
    result = _analyze_code("")
    assert result["metrics"]["lines"] == 1
    assert isinstance(result["score"], int)


def test_analyze_code_unused_import():
    code = "import os\nx = 1\nprint(x)"
    result = _analyze_code(code)
    assert result["metrics"]["imports"] == 1
    assert isinstance(result["score"], int)
