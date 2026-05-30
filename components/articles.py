# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary

@error_boundary
def render_articles():
    articles = PORTFOLIO_DATA["articles"]

    st.markdown('<div class="section-header">Articles & Writing</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Technical write-ups on AI, Python engineering, and software design.</p>",
        unsafe_allow_html=True
    )

    for i in range(0, len(articles), 2):
        cols = st.columns(2, gap="large")
        for j in range(2):
            if i + j < len(articles):
                art = articles[i + j]
                with cols[j]:
                    # Colour-coded category accent
                    cat_colors = {
                        "Artificial Intelligence": "#4F7CFF",
                        "Software Engineering":    "#00D4FF",
                        "Python & Software Design": "#a78bfa",
                    }
                    cat_color = cat_colors.get(art["category"], "#4F7CFF")

                    st.markdown(f"""
                    <div class="glass-card" style="display: flex; flex-direction: column; justify-content: space-between; height: 100%;">
                        <!-- Coloured category banner -->
                        <div style="height: 6px; border-radius: 6px 6px 0 0; background: {cat_color};
                                    margin: -24px -24px 20px -24px; border-radius: 15px 15px 0 0;"></div>

                        <div>
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
                        </div>

                        <div style="display: flex; align-items: center; justify-content: space-between; font-size: 0.82rem; color: var(--text-muted);">
                            <span>📅 {art['date']}</span>
                            <span>⏱ {art['read_time']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # Newsletter / follow CTA
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 32px;">
        <div style="font-size: 2rem; margin-bottom: 10px;">✍️</div>
        <h4 style="color: var(--text-color); font-weight: 700; font-size: 1.4rem; margin-bottom: 8px;">
            More articles coming soon
        </h4>
        <p style="color: var(--text-muted); font-size: 0.95rem; margin-bottom: 0; max-width: 480px; margin: 0 auto;">
            I publish deep-dives on AI systems design, Python architecture, and
            software engineering best practices. Follow on LinkedIn or GitHub to stay updated.
        </p>
    </div>
    """, unsafe_allow_html=True)
