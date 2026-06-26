# -*- coding: utf-8 -*-
import streamlit as st
import ast
from io import BytesIO
import pandas as pd
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html

def _profile_csv(file_bytes: bytes) -> dict:
    """Analyse a CSV file with pandas. Returns dict with profile or error."""
    try:
        df = pd.read_csv(BytesIO(file_bytes))
    except Exception as e:
        return {"success": False, "error": f"Could not read CSV: {e}"}

    total_cells = df.size
    null_cells = df.isnull().sum().sum()
    completeness = round((1 - null_cells / total_cells) * 100, 1) if total_cells else 100.0

    columns = []
    for col in df.columns:
        info = {
            "name": col,
            "dtype": str(df[col].dtype),
            "nulls": int(df[col].isnull().sum()),
            "null_pct": round(float(df[col].isnull().mean() * 100), 1),
            "uniques": int(df[col].nunique()),
            "sample": str(df[col].dropna().iloc[0]) if df[col].count() > 0 else "",
        }
        if pd.api.types.is_numeric_dtype(df[col]):
            info["min"] = round(float(df[col].min()), 4) if df[col].count() > 0 else None
            info["max"] = round(float(df[col].max()), 4) if df[col].count() > 0 else None
            info["mean"] = round(float(df[col].mean()), 4) if df[col].count() > 0 else None
        columns.append(info)

    score = 100
    if completeness < 80:
        score -= 20
    elif completeness < 95:
        score -= 10
    if df.duplicated().sum() > 0:
        score -= 10
    if len(df.columns) < 2:
        score -= 10
    score = max(0, score)

    return {
        "success": True,
        "rows": len(df),
        "cols": len(df.columns),
        "columns": columns,
        "duplicates": int(df.duplicated().sum()),
        "completeness": completeness,
        "score": score,
        "preview": df.head(10).to_html(classes="data-preview", index=False),
    }


def _analyze_code(code_str: str) -> dict:
    """Analyze Python code using AST. Returns metrics and issues."""
    issues = []
    metrics = {
        "lines": len(code_str.split("\n")),
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "has_type_hints": False,
        "has_docstrings": False,
        "bare_excepts": 0,
        "complexity": 0,
    }

    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax Error: {e}", "metrics": metrics, "issues": [str(e)], "score": 0}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            metrics["functions"] += 1
            if node.returns or any(arg.annotation for arg in node.args.args):
                metrics["has_type_hints"] = True
            if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, (ast.Constant, ast.Str))):
                metrics["has_docstrings"] = True
            if not node.name.islower() and "_" not in node.name:
                issues.append(f"Function '{node.name}' should use snake_case")

        elif isinstance(node, ast.ClassDef):
            metrics["classes"] += 1

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            metrics["imports"] += 1

        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            metrics["bare_excepts"] += 1
            issues.append("Bare except clause detected — specify exception type")

    complexity_nodes = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.BoolOp)
    metrics["complexity"] = sum(1 for _ in ast.walk(tree) if isinstance(_, complexity_nodes))

    score = 100
    if metrics["bare_excepts"] > 0:
        score -= metrics["bare_excepts"] * 10
    if not metrics["has_type_hints"]:
        score -= 15
    if not metrics["has_docstrings"]:
        score -= 10
    if metrics["complexity"] > 20:
        score -= 10
    if metrics["functions"] == 0 and metrics["classes"] == 0:
        score -= 5
    if metrics["imports"] > 0 and metrics["has_type_hints"] and metrics["has_docstrings"]:
        score = min(score + 5, 100)
    score = max(0, min(100, score))

    return {"metrics": metrics, "issues": issues, "score": score}


@error_boundary
def render_playground() -> None:
    render_html('<div class="section-header">Interactive Playground</div>')
    render_html(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Practical tools that demonstrate real engineering — file processing, data profiling, and static code analysis.</p>"
    )

    tab_csv, tab_code = st.tabs([
        "📊 CSV Profiler",
        "🔍 Code Analyser",
    ])

    # ── Tab 1: CSV Profiler ─────────────────────────────────────────────────
    with tab_csv:
        render_html("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">📊 CSV Data Profiler</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Upload a CSV file for automatic profiling — column types, null analysis, uniqueness,
                summary statistics, and a data quality score.
            </p>
        </div>
        """)

        csv_file = st.file_uploader("Upload a CSV file", type=["csv"], key="csv_upload", label_visibility="collapsed")

        if csv_file:
            csv_bytes = csv_file.getvalue()
            render_html(f"""
            <div class="glass-card" style="margin: 20px 0;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="font-size: 2rem;">📋</div>
                    <div>
                        <div style="font-weight: 700; color: var(--text-color);">{csv_file.name}</div>
                        <div style="color: var(--text-muted); font-size: 0.88rem;">{len(csv_bytes) / 1024:.1f} KB</div>
                    </div>
                </div>
            </div>
            """)

            if st.button("📊 Profile CSV", type="primary", key="profile_btn"):
                with st.spinner("Profiling..."):
                    profile = _profile_csv(csv_bytes)

                if not profile["success"]:
                    st.error(profile["error"])
                else:
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Rows", f"{profile['rows']:,}")
                    col2.metric("Columns", profile["cols"])
                    col3.metric("Completeness", f"{profile['completeness']}%")
                    col4.metric("Duplicates", profile["duplicates"])

                    score = profile["score"]
                    color = "var(--color-success)" if score >= 80 else "var(--color-warning)" if score >= 60 else "var(--color-error)"
                    render_html(f'<div style="text-align:center; font-size:2.5rem; font-weight:800; color:{color}; margin:16px 0 4px;">{score}/100</div>')
                    render_html('<div style="text-align:center; color:var(--text-muted); margin-bottom:20px;">Data Quality Score</div>')

                    st.markdown("**Column Profile**")
                    cols_data = []
                    for c in profile["columns"]:
                        row = {
                            "Column": c["name"],
                            "Type": c["dtype"],
                            "Nulls": f'{c["nulls"]} ({c["null_pct"]}%)',
                            "Unique": c["uniques"],
                            "Sample": c["sample"][:60],
                        }
                        if c.get("mean") is not None:
                            row["Mean"] = c["mean"]
                            row["Min"] = c["min"]
                            row["Max"] = c["max"]
                        cols_data.append(row)
                    st.dataframe(pd.DataFrame(cols_data), use_container_width=True, hide_index=True)

                    st.markdown("**Data Preview (first 10 rows)**")
                    st.markdown(profile["preview"], unsafe_allow_html=True)
        else:
            render_html("""
            <div style="text-align: center; padding: 50px 20px; color: var(--text-muted); font-size: 0.95rem;">
                <div style="font-size: 3rem; margin-bottom: 14px;">📂</div>
                Upload a CSV file to generate a profile.
            </div>
            """)

    # ── Tab 2: Code Analyser ─────────────────────────────────────────────────
    with tab_code:
        render_html("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">🔍 Python Code Analyser</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Paste Python code below for real AST-based static analysis — function/class counts, type hints,
                docstrings, complexity estimation, and quality scoring.
            </p>
        </div>
        """)

        default_code = '''def process(data):
    try:
        result = [x * 2 for x in data]
        print("Done:", result)
        return result
    except:
        print("Error occurred")
'''

        code_input = st.text_area(
            "Paste your Python code:",
            value=default_code,
            height=220,
            key="code_analyser_input"
        )

        if st.button("🔎 Analyse Code", type="primary", key="analyse_code_btn"):
            if not code_input.strip():
                st.warning("Please paste some Python code to analyse.")
            else:
                with st.spinner("Running static analysis..."):
                    result = _analyze_code(code_input)

                if "error" in result:
                    st.error(result["error"])
                else:
                    score = result["score"]
                    color = "var(--color-success)" if score >= 80 else "var(--color-warning)" if score >= 60 else "var(--color-error)"
                    render_html(f'<div style="text-align:center; font-size:3rem; font-weight:800; color:{color};">{score}/100</div>')
                    render_html('<div style="text-align:center; color:var(--text-muted); margin-bottom:20px;">Code Quality Score</div>')

                    m = result["metrics"]
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Lines", m["lines"])
                    col2.metric("Functions", m["functions"])
                    col3.metric("Classes", m["classes"])
                    col4.metric("Complexity", m["complexity"])

                    if result["issues"]:
                        st.markdown("**Issues Found:**")
                        for issue in result["issues"]:
                            st.warning(issue)
                    else:
                        st.success("No issues found!")
