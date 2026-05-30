# -*- coding: utf-8 -*-
import streamlit as st
from utils.helpers import error_boundary, load_articles


@error_boundary
def render_articles() -> None:
    """Render the Articles section from markdown files."""
    articles = load_articles()

    st.markdown('<div class="section-header">Articles & Writing</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Technical write-ups on AI, Python engineering, and software design.</p>",
        unsafe_allow_html=True
    )

    if not articles:
        st.info("Articles coming soon!")
        return

    # Category filter
    categories = ["All"] + sorted(set(a["category"] for a in articles))
    selected = st.pills("Filter by category", categories, selection_mode="single", default="All")

    filtered = articles if selected == "All" else [a for a in articles if a["category"] == selected]

    # Category colors
    cat_colors = {
        "Artificial Intelligence": "#4F7CFF",
        "Software Engineering": "#00D4FF",
        "Python & Software Design": "#a78bfa",
    }

    # Article cards in 2-column layout
    for i in range(0, len(filtered), 2):
        cols = st.columns(2, gap="large")
        for j in range(2):
            if i + j < len(filtered):
                art = filtered[i + j]
                cat_color = cat_colors.get(art["category"], "#4F7CFF")
                with cols[j]:
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="height: 6px; border-radius: 15px 15px 0 0; background: {cat_color};
                                    margin: -24px -24px 20px -24px;"></div>
                        <span style="font-size: 0.75rem; font-weight: 700; color: {cat_color};
                                     text-transform: uppercase; letter-spacing: 0.06em;">
                            {art['category']}
                        </span>
                        <h3 style="font-size: 1.2rem; font-weight: 700; color: var(--text-color);
                                    margin: 10px 0 10px 0; line-height: 1.3;">
                            {art['title']}
                        </h3>
                        <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.55; margin-bottom: 18px;">
                            {art['excerpt']}
                        </p>
                        <div style="display: flex; align-items: center; justify-content: space-between;
                                    font-size: 0.82rem; color: var(--text-muted);">
                            <span>📅 {art['date']}</span>
                            <span>⏱ {art['read_time']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Expanders below the row to avoid overlap
        for j in range(2):
            if i + j < len(filtered):
                art = filtered[i + j]
                with st.expander(f"Read: {art['title']}", expanded=False):
                    st.markdown(art.get("content", art["excerpt"]))

    # CTA
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 32px; margin-top: 20px;">
        <div style="font-size: 2rem; margin-bottom: 10px;">✍️</div>
        <h4 style="color: var(--text-color); font-weight: 700; font-size: 1.4rem; margin-bottom: 8px;">
            More articles coming soon
        </h4>
        <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 480px; margin: 0 auto;">
            Follow on LinkedIn or GitHub to stay updated.
        </p>
    </div>
    """, unsafe_allow_html=True)
