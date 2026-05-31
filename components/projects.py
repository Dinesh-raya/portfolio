# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import github_fetch_repos, error_boundary, render_html


@error_boundary
def render_projects() -> None:
    """Render the Projects section from live GitHub repositories."""
    personal = PORTFOLIO_DATA["personal"]

    render_html('<div class="section-header">Projects & Work</div>')
    render_html("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 25px;'>Live repositories fetched from GitHub — no fake data, just real projects I've built.</p>")

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
                                    <span style="color: var(--text-muted);">⭐ {repo.get('stargazers_count', 0)} stars</span>
                                    <span style="color: var(--text-muted);">🍴 {repo.get('forks_count', 0)} forks</span>
                                </div>
                                <a href="{repo['html_url']}" target="_blank" class="custom-btn" style="padding: 6px 14px; font-size: 0.85rem; width: 100%; text-align: center;">🌐 View Repository</a>
                            </div>
                        </div>
                        """)
                        render_html("<div style='height: 15px;'></div>")
    else:
        st.warning(
            f"Could not fetch repositories from GitHub right now. "
            f"Visit [GitHub profile]({personal['github']}) directly."
        )
