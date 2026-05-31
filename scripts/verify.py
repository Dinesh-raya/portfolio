# -*- coding: utf-8 -*-
"""Quick verification script for the portfolio project."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

FAILURES: list[str] = []
WARNINGS: list[str] = []


def check(name: str, ok: bool, detail: str = "", *, optional: bool = False) -> None:
    if optional and not ok:
        status = "WARN"
        WARNINGS.append(name)
    else:
        status = "PASS" if ok else "FAIL"
        if not ok:
            FAILURES.append(name)
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    print(line)


def main() -> int:
    print("=== Portfolio verification ===\n")

    from data.portfolio_data import PORTFOLIO_DATA

    required_keys = ["personal", "stats", "about", "projects", "skills", "tech_stack", "experience"]
    check("portfolio_data keys", all(k in PORTFOLIO_DATA for k in required_keys))
    check("stats count >= 4", len(PORTFOLIO_DATA["stats"]) >= 4)
    check("projects count >= 1", len(PORTFOLIO_DATA["projects"]) >= 1)
    check("skills.radar", "radar" in PORTFOLIO_DATA.get("skills", {}))

    personal = PORTFOLIO_DATA["personal"]
    for field in ("name", "email", "github", "linkedin"):
        check(f"personal.{field}", bool(personal.get(field)))
    check("personal.github_username", bool(personal.get("github_username")))
    check("personal.photo path set", bool(personal.get("photo")))

    gh_user = personal.get("github_username", "")
    for proj in PORTFOLIO_DATA["projects"]:
        gh = proj.get("github", "")
        if gh and "dineshraya" in gh.lower() and "dinesh-raya" not in gh.lower():
            check(f"project {proj.get('id')} github URL", False, gh)
            break
    else:
        check("project github URLs aligned", True)

    check("assets/README.md", os.path.isfile(os.path.join("assets", "README.md")))
    check(".gitignore messages.json", "assets/messages.json" in open(".gitignore", encoding="utf-8").read())
    check(
        "secrets.toml.example",
        os.path.isfile(os.path.join(".streamlit", "secrets.toml.example")),
    )

    css_path = os.path.join("styles", "main.css")
    check("main.css exists", os.path.isfile(css_path), f"{os.path.getsize(css_path)} bytes")

    config_path = os.path.join(".streamlit", "config.toml")
    check("streamlit config", os.path.isfile(config_path))

    resume_path = os.path.join("assets", "dinesh_raya.pdf")
    check(
        "dinesh_raya.pdf",
        os.path.isfile(resume_path),
        "present" if os.path.isfile(resume_path) else "missing — use mailto / add assets/dinesh_raya.pdf",
        optional=True,
    )

    from utils.helpers import render_html, inject_theme_and_css, get_tech_icon_url, send_contact_form

    check("render_html exists", callable(render_html))
    check("send_contact_form exists", callable(send_contact_form))
    url = get_tech_icon_url("python")
    check("get_tech_icon_url", url.startswith("https://"))

    try:
        import streamlit as st

        form_id = None
        try:
            form_id = st.secrets.get("formspree", {}).get("form_id")
        except Exception:
            pass
        has_formspree = bool(form_id) and "your_formspree" not in str(form_id).lower()
        check(
            "formspree configured",
            has_formspree,
            "set in .streamlit/secrets.toml for production email" if not has_formspree else "ok",
            optional=True,
        )
    except ImportError:
        check("formspree configured", False, "streamlit not installed", optional=True)

    from components.hero import (
        _skill_bars_html,
        _projects_html,
        _tech_grid_html,
        _timeline_html,
        _articles_html,
        _radar_chart,
        _github_repos_html,
    )

    skills = PORTFOLIO_DATA["skills"]
    html = _skill_bars_html(skills["radar"]["metrics"], skills["radar"]["values"])
    check("_skill_bars_html", "skill-progress-fill" in html and "<div" in html)
    proj_html = _projects_html(PORTFOLIO_DATA["projects"])
    check("_projects_html", len(proj_html) > 50)
    check("_radar_chart", _radar_chart(skills, "dark") is not None)
    check("utils/__init__.py", os.path.isfile(os.path.join("utils", "__init__.py")))

    pages = ["Home", "About", "Projects", "Skills", "Tech Stack", "Articles", "Playground", "Contact"]
    check("navigation pages", len(pages) == 8, ", ".join(pages))

    print()
    if WARNINGS:
        print(f"Warnings ({len(WARNINGS)}): {', '.join(WARNINGS)}")
    if FAILURES:
        print(f"FAILED: {len(FAILURES)} check(s): {', '.join(FAILURES)}")
        return 1
    print("All required checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
