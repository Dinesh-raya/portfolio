# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html
from utils.icons import icon


@error_boundary
def render_contact() -> None:
    """Render the Contact section with direct contact info — no external forms."""
    personal = PORTFOLIO_DATA["personal"]
    gh_user = personal.get("github_username", "Dinesh-raya")

    render_html('<div class="section-header">Contact & Connect</div>')
    render_html(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Have a project idea, collaboration proposal, or just want to say hi? I'd love to hear from you.</p>"
    )

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        render_html(f"""
        <a href="mailto:{personal['email']}" style="text-decoration: none;">
            <div class="glass-card" style="text-align: center; padding: 36px 24px; cursor: pointer;">
                <div style="margin-bottom: 12px;">{icon("mail", 44)}</div>
                <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.2rem; margin-bottom: 8px;">
                    Send me an email
                </h4>
                <div style="color: var(--text-color); font-size: 1.05rem; font-weight: 600;">
                    {personal['email']}
                </div>
                <div style="color: var(--text-muted); font-size: 0.85rem; margin-top: 8px;">
                    I typically respond within 24 hours.
                </div>
            </div>
        </a>
        """)

    with col2:
        contacts = [
            ("LinkedIn", f"linkedin.com/in/{personal['linkedin'].rstrip('/').split('/')[-1]}", personal["linkedin"]),
            ("GitHub", f"github.com/{gh_user}", personal["github"]),
            ("Location", personal["location"], "#"),
        ]

        for label, value, link in contacts:
            href = f'href="{link}" target="_blank"' if link != "#" else ""
            cursor = "pointer" if link != "#" else "default"
            render_html(f"""
            <a {href} style="text-decoration: none;">
                <div class="glass-card" style="display: flex; align-items: center; gap: 16px;
                                                cursor: {cursor}; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em;
                                    color: var(--text-muted); font-weight: 600; margin-bottom: 2px;">{label}</div>
                        <div style="font-weight: 600; color: var(--text-color); font-size: 0.95rem;">{value}</div>
                    </div>
                </div>
            </a>
            """)

        render_html("""
        <div class="glass-card" style="text-align: center; margin-top: 8px; padding: 20px;">
            <div class="status-badge-available">
                <span class="status-dot"></span>
                Available for freelance and collaboration
            </div>
        </div>
        """)
