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

    # Category filter
    categories = ["All"] + sorted(set(a["category"] for a in articles))
    selected = st.pills("Filter by category", categories, selection_mode="single", default="All")

    filtered = articles if selected == "All" else [a for a in articles if a["category"] == selected]

    cat_colors = {
        "Artificial Intelligence": "#4F7CFF",
        "Software Engineering": "#00D4FF",
        "Python & Software Design": "#a78bfa",
    }

    # Track which article to read
    if "article_to_read" not in st.session_state:
        st.session_state.article_to_read = None

    # Article cards in 2-column layout
    for i in range(0, len(filtered), 2):
        cols = st.columns(2, gap="large")
        for j in range(2):
            if i + j < len(filtered):
                art = filtered[i + j]
                cat_color = cat_colors.get(art["category"], "#4F7CFF")
                art_idx = i + j
                with cols[j]:
                    render_html(f"""
                    <div class="glass-card" style="padding-bottom: 16px;">
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
                        <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; margin-bottom: 12px;">
                            {art['excerpt']}
                        </p>
                        <div style="display: flex; align-items: center; justify-content: space-between;
                                    font-size: 0.8rem; color: var(--text-muted);">
                            <span>📅 {art['date']}</span>
                            <span>⏱ {art['read_time']}</span>
                        </div>
                    </div>
                    """)
                    if st.button(f"Read More →", key=f"read_{art_idx}"):
                        st.session_state.article_to_read = art_idx
                        st.rerun()

    # Show selected article content below the grid
    art_idx = st.session_state.article_to_read
    if art_idx is not None and art_idx < len(filtered):
        art = filtered[art_idx]
        st.divider()
        render_html(f"""
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
            <h3 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin: 0;">{art['title']}</h3>
        </div>
        <div style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 16px;">
            {art['category']} — 📅 {art['date']} — ⏱ {art['read_time']}
        </div>
        """)
        st.markdown(art.get("content", art["excerpt"]))
        if st.button("← Back to Articles", key="close_article"):
            st.session_state.article_to_read = None
            st.rerun()
