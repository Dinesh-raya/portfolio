# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html

@error_boundary
def render_about() -> None:
    """Render the About section with professional summary and credentials."""
    about_data = PORTFOLIO_DATA["about"]
    personal = PORTFOLIO_DATA["personal"]
    
    render_html('<div class="section-header">About Me</div>')
    render_html("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>My engineering background, journey, and developer setup.</p>")
    
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    
    with col1:
        render_html(f"""
        <div class="glass-card" style="margin-bottom: 25px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🎯</span> Professional Summary
            </h4>
            <p style="color: var(--text-color); font-size: 1.05rem; line-height: 1.6; margin: 0;">
                {about_data['summary']}
            </p>
        </div>
        
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🚀</span> My Coding Journey
            </h4>
            <p style="color: var(--text-muted); font-size: 1rem; line-height: 1.6; margin: 0;">
                {about_data['journey']}
            </p>
        </div>
        """)
        
    with col2:
        # Info Card
        render_html(f"""
        <div class="glass-card" style="margin-bottom: 25px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>ℹ️</span> Details & Credentials
            </h4>
            <div style="display: grid; gap: 15px;">
                <div>
                    <strong style="color: var(--text-color);">📍 Location:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">{personal['location']}</div>
                </div>
                <div>
                    <strong style="color: var(--text-color);">📧 Email:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">
                        <a href="mailto:{personal['email']}" style="color: var(--accent-color); text-decoration: none;">{personal['email']}</a>
                    </div>
                </div>
                <div>
                    <strong style="color: var(--text-color);">🗣️ Languages:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">{", ".join(about_data['languages'])}</div>
                </div>
            </div>
        </div>
        """)
        
        # Education Card
        edu_html = ""
        for edu in about_data["education"]:
            edu_html += f"""
            <div style="margin-bottom: 10px;">
                <div style="font-weight: 600; color: var(--text-color);">{edu['degree']}</div>
                <div style="font-size: 0.9rem; color: var(--accent-color);">{edu['institution']}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">{edu['year']}</div>
            </div>
            """
            
        render_html(f"""
        <div class="glass-card" style="margin-bottom: 25px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>🎓</span> Education
            </h4>
            {edu_html}
        </div>
        """)
        
        # Workspace Preferences
        ws = about_data["workspace_info"]
        render_html(f"""
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>💻</span> Workspace Setup
            </h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.95rem;">
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">OS</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['os']}</div>
                </div>
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Editor</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['editor']}</div>
                </div>
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Terminal</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['terminal']}</div>
                </div>
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Vibe</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['vibe']}</div>
                </div>
            </div>
        </div>
        """)

    # ── Journey & Highlights (merged from Experience tab) ─────────────────────
    render_html("<div style='height: 40px;'></div>")
    render_html("""
    <div style="height: 1px; background: linear-gradient(90deg, transparent, var(--border-color), var(--accent-color), var(--border-color), transparent); margin-bottom: 40px;"></div>
    """)

    render_html("""
    <h2 style="font-size: 2rem; font-weight: 800; margin-bottom: 8px;">
        My <span style="background: linear-gradient(45deg, var(--accent-color), var(--accent-secondary)); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Journey</span>
    </h2>
    <p style="color: var(--text-muted); font-size: 1.05rem; margin-bottom: 30px;">
        A brief look at my path — from foundations to real-world AI engineering.
    </p>
    """)

    exp_data = PORTFOLIO_DATA.get("experience", [])
    if exp_data:
        j_col1, j_col2 = st.columns([0.03, 0.97])
        with j_col2:
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
            timeline_html += "</div>"
            render_html(timeline_html)

    # Key highlights strip
    highlights = PORTFOLIO_DATA.get("highlights", [])
    if highlights:
        render_html("<div style='height: 36px;'></div>")
        render_html('<h3 style="font-size: 1.4rem; font-weight: 700; color: var(--text-color); margin-bottom: 20px;">📌 Key Highlights</h3>')
        h_cols = st.columns(len(highlights), gap="medium")
        for i, item in enumerate(highlights):
            with h_cols[i]:
                render_html(f"""
                <div class="glass-card" style="text-align: center; padding: 20px 14px;">
                    <div style="font-size: 2rem; margin-bottom: 10px;">{item['icon']}</div>
                    <div style="font-weight: 700; font-size: 1rem; color: var(--text-color); margin-bottom: 6px;">{item['title']}</div>
                    <div style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.45;">{item['desc']}</div>
                </div>
                """)

