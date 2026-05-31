# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import get_tech_icon_url, error_boundary, render_html

@error_boundary
def render_tech_stack() -> None:
    """Render the Tech Stack section with technology icons."""
    tech_data = PORTFOLIO_DATA["tech_stack"]

    render_html('<div class="section-header">Tech Stack</div>')
    render_html(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Languages, frameworks, tools and databases I work with daily.</p>"
    )

    for group in tech_data:
        render_html(
            f"<h4 style='color: var(--accent-color); font-weight: 700; font-size: 1.2rem; "
            f"margin-bottom: 18px; margin-top: 10px;'>⚙️ {group['category']}</h4>"
        )

        num_items = len(group["items"])
        num_cols = min(num_items, 4)
        cols = st.columns(num_cols, gap="small")
        for idx, item in enumerate(group["items"]):
            icon_url = get_tech_icon_url(item["icon_svg"])
            with cols[idx % num_cols]:
                render_html(f"""
                <div class="tech-icon-card">
                    <img src="{icon_url}" width="44" height="44" loading="lazy"
                         style="object-fit: contain;"
                         onerror="this.style.display='none'"
                         alt="{item['name']}" />
                    <div class="tech-icon-name">{item['name']}</div>
                </div>
                """)

        render_html("<div style='height: 28px;'></div>")
