# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html

@error_boundary
def render_experience() -> None:
    """Render the Experience section with timeline layout."""
    exp_data = PORTFOLIO_DATA["experience"]

    st.markdown('<div class="section-header">Experience & Journey</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Key milestones in my engineering and AI development path.</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([0.05, 0.95])
    with col2:
        timeline_html = '<div class="timeline">'
        for item in exp_data:
            timeline_html += f"""
            <div class="timeline-item">
                <div class="timeline-date">{item['period']}</div>
                <div class="timeline-title">{item['title']}</div>
                <div class="timeline-subtitle">{item['subtitle']}</div>
                <div class="timeline-desc">{item['description']}</div>
            </div>
            """
        timeline_html += '</div>'
        render_html(timeline_html)

    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Additional quick-facts strip
    st.markdown('<h4 style="color: var(--text-color); font-weight: 700; font-size: 1.2rem; margin-bottom: 16px;">📌 Key Highlights</h4>', unsafe_allow_html=True)
    highlights = PORTFOLIO_DATA.get("highlights", [])
    h_cols = st.columns(2, gap="small")
    for i, item in enumerate(highlights):
        icon = item["icon"]
        title = item["title"]
        desc = item["desc"]
        with h_cols[i % 2]:
            st.markdown(f"""
            <div class="glass-card" style="text-align: center; padding: 18px 12px;">
                <div style="font-size: 1.8rem; margin-bottom: 8px;">{icon}</div>
                <div style="font-weight: 700; font-size: 1rem; color: var(--text-color); margin-bottom: 6px;">{title}</div>
                <div style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.4;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
