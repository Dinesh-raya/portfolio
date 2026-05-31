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

    search = st.text_input("🔍", placeholder="Search articles by title or excerpt...", label_visibility="collapsed")

    filtered = articles if selected == "All" else [a for a in articles if a["category"] == selected]
    if search:
        q = search.lower()
        filtered = [a for a in filtered if q in a["title"].lower() or q in a["excerpt"].lower()]

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
                art_key = f"art_open_{i + j}"
                img_tag = ""
                if art.get("image"):
                    img_tag = f'<img src="{art["image"]}" alt="{art["title"]}" class="article-thumb" loading="lazy" />'
                else:
                    initial = art["title"][0].upper() if art["title"] else "?"
                    img_tag = f'<div class="article-thumb-fallback" style="background: linear-gradient(135deg, {cat_color}, {cat_color}88);"><span>{initial}</span></div>'
                with cols[j]:
                    render_html(f"""
                    <div class="glass-card" style="padding-bottom: 12px;">
                        {img_tag}
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
                    is_open = st.session_state.get(art_key, False)
                    label = "Close" if is_open else "Read More"
                    if st.button(label, key=f"btn_{art_key}", use_container_width=True):
                        st.session_state[art_key] = not is_open
                        st.rerun()
                    if is_open:
                        st.markdown(art.get("content", art["excerpt"]))
