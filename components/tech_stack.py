# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import get_tech_icon_url, error_boundary

@error_boundary
def render_tech_stack() -> None:
    """Render the Tech Stack section with technology icons."""
    tech_data = PORTFOLIO_DATA["tech_stack"]

    st.markdown('<div class="section-header">Tech Stack</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Languages, frameworks, tools and databases I work with daily.</p>",
        unsafe_allow_html=True
    )

    for group in tech_data:
        st.markdown(
            f"<h4 style='color: var(--accent-color); font-weight: 700; font-size: 1.2rem; "
            f"margin-bottom: 18px; margin-top: 10px;'>⚙️ {group['category']}</h4>",
            unsafe_allow_html=True
        )

        num_items = len(group["items"])
        num_cols = min(num_items, 4)
        cols = st.columns(num_cols, gap="small")
        for idx, item in enumerate(group["items"]):
            icon_url = get_tech_icon_url(item["icon_svg"])
            with cols[idx % num_cols]:
                st.markdown(f"""
                <div class="tech-icon-card">
                    <img src="{icon_url}" width="44" height="44"
                         style="object-fit: contain;"
                         onerror="this.style.display='none'"
                         alt="{item['name']}" />
                    <div class="tech-icon-name">{item['name']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
