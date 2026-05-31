# -*- coding: utf-8 -*-
import streamlit as st
from utils.helpers import error_boundary, load_articles, render_html


@error_boundary
def render_articles() -> None:
    """Render the Articles section from markdown files."""
    articles = load_articles()

    render_html('<div class="section-header">Articles & Writing</div>')
    render_html(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Technical write-ups on AI, Python engineering, and software design.</p>"
    )

    if not articles:
        st.info("Articles coming soon!")
        return

    categories = ["All"] + sorted(set(a["category"] for a in articles))
    selected = st.pills("Filter by category", categories, selection_mode="single", default="All")

    filtered = articles if selected == "All" else [a for a in articles if a["category"] == selected]

    cat_colors = {
        "Artificial Intelligence": "#4F7CFF",
        "Software Engineering": "#00D4FF",
        "Python & Software Design": "#a78bfa",
    }

    for i in range(0, len(filtered), 2):
        cols = st.columns(2, gap="large")
        for j in range(2):
            if i + j < len(filtered):
                art = filtered[i + j]
                cat_color = cat_colors.get(art["category"], "#4F7CFF")
                with cols[j]:
                    render_html(f"""
                    <div class="glass-card" style="padding-bottom: 12px;">
                        <div style="height: 5px; border-radius: 15px 15px 0 0; background: {cat_color};
                                    margin: -24px -24px 18px -24px;"></div>
                        <span style="font-size: 0.72rem; font-weight: 700; color: {cat_color};
                                     text-transform: uppercase; letter-spacing: 0.06em;">
                            {art['category']}
                        </span>
                        <h3 style="font-size: 1.1rem; font-weight: 700; color: var(--text-color);
                                    margin: 8px 0 8px 0; line-height: 1.3;">
                            {art['title']}
                        </h3>
                        <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; margin-bottom: 10px;">
                            {art['excerpt']}
                        </p>
                        <div style="display: flex; align-items: center; justify-content: space-between;
                                    font-size: 0.8rem; color: var(--text-muted); margin-bottom: 10px;">
                            <span>📅 {art['date']}</span>
                            <span>⏱ {art['read_time']}</span>
                        </div>
                    </div>
                    """)
                    with st.popover("Read More →", use_container_width=True):
                        st.markdown(f"### {art['title']}")
                        render_html(f"<div style='color: var(--text-muted); font-size: 0.85rem; margin-bottom: 12px;'>{art['category']} — 📅 {art['date']} — ⏱ {art['read_time']}</div>")
                        st.markdown(art.get("content", art["excerpt"]))
