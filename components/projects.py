# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import github_fetch_repos, error_boundary, render_html
from utils.icons import icon


@error_boundary
def render_projects() -> None:
    """Render the Projects section with filtering and GitHub integration."""
    projects_list = PORTFOLIO_DATA["projects"]
    personal = PORTFOLIO_DATA["personal"]

    if "proj_filter" not in st.session_state:
        st.session_state.proj_filter = "All"

    render_html('<div class="section-header">Projects & Work</div>')
    render_html("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 25px;'>Real projects I've built — with live demos and source code.</p>")

    view_mode = st.radio(
        "Select View Mode",
        options=["Featured Projects", "Live GitHub Activity"],
        horizontal=True,
        label_visibility="collapsed"
    )

    render_html("<div style='height: 15px;'></div>")

    if view_mode == "Featured Projects":
        categories = ["All"] + sorted(set(p["category"] for p in projects_list))

        pill_cols = st.columns(len(categories))
        for idx, cat in enumerate(categories):
            with pill_cols[idx]:
                if st.button(cat, key=f"proj_cat_{cat}", width="stretch"):
                    st.session_state.proj_filter = cat
                    st.rerun()

        selected_category = st.session_state.proj_filter
        render_html("<div style='height: 25px;'></div>")

        if selected_category == "All":
            filtered_projects = projects_list
        else:
            filtered_projects = [p for p in projects_list if p["category"] == selected_category]

        for i in range(0, len(filtered_projects), 2):
            cols = st.columns(2, gap="large")
            for j in range(2):
                if i + j < len(filtered_projects):
                    proj = filtered_projects[i + j]
                    with cols[j]:
                        tags_html = "".join([f'<span class="tech-tag">{tag}</span>' for tag in proj["tech"]])
                        demo_btn_html = ""
                        if proj.get("demo") and proj["demo"] not in ("#", ""):
                            demo_btn_html = f'<a href="{proj["demo"]}" target="_blank" class="custom-btn" style="padding: 6px 14px; font-size: 0.85rem; margin-right: 8px;">{icon("rocket", 16)} Live Demo</a>'

                        render_html(f"""
                        <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                            <div>
                                <div style="height: 100px; border-radius: 8px; background: linear-gradient(135deg, var(--surface-subtle), var(--card-bg)); border: 1px solid var(--border-color); display: flex; align-items: center; justify-content: center; margin-bottom: 16px;">
                                    <div style="font-size: 2.2rem;">{icon("wrench", 28)}</div>
                                </div>
                                <h3 style="font-weight: 700; font-size: 1.4rem; color: var(--text-color); margin-bottom: 8px;">{proj['title']}</h3>
                                <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--accent-color); font-weight: 700; letter-spacing: 0.05em; margin-bottom: 12px;">{proj['category']}</div>
                                <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.5; margin-bottom: 16px; min-height: 70px;">{proj['description']}</p>
                            </div>
                            <div>
                                <div style="margin-bottom: 20px;">{tags_html}</div>
                                <div style="display: flex; align-items: center;">
                                    {demo_btn_html}
                                    <a href="{proj['github']}" target="_blank" class="custom-btn-outline" style="padding: 5px 12px; font-size: 0.85rem;">{icon("external-link", 14)} GitHub</a>
                                </div>
                            </div>
                        </div>
                        """)
                        render_html("<div style='height: 15px;'></div>")

    elif view_mode == "Live GitHub Activity":
        username = personal.get("github_username") or personal["github"].rstrip("/").split("/")[-1]
        repos = github_fetch_repos(username)

        if repos:
            for i in range(0, len(repos), 2):
                cols = st.columns(2, gap="large")
                for j in range(2):
                    if i + j < len(repos):
                        repo = repos[i + j]
                        with cols[j]:
                            lang = repo.get("language", "Python")
                            render_html(f"""
                            <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
                                <div>
                                    <h3 style="font-weight: 700; font-size: 1.3rem; color: var(--text-color); margin-bottom: 8px;">{repo['name']}</h3>
                                    <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; margin-bottom: 16px; min-height: 50px;">
                                        {repo.get('description') or 'No description provided.'}
                                    </p>
                                </div>
                                <div>
                                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 16px; font-size: 0.85rem;">
                                        <span class="tech-tag" style="margin-bottom: 0;">{lang}</span>
                                        <span style="color: var(--text-muted);">{icon("star", 14)} {repo.get('stargazers_count', 0)} stars</span>
                                        <span style="color: var(--text-muted);">{icon("git-fork", 14)} {repo.get('forks_count', 0)} forks</span>
                                    </div>
                                    <a href="{repo['html_url']}" target="_blank" class="custom-btn" style="padding: 6px 14px; font-size: 0.85rem; width: 100%; text-align: center;">{icon("external-link", 14)} View Repository</a>
                                </div>
                            </div>
                            """)
                            render_html("<div style='height: 15px;'></div>")
        else:
            st.warning(
                f"Could not fetch repositories from GitHub right now. "
                f"Visit [GitHub profile]({personal['github']}) directly."
            )
