# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html
from utils.icons import icon


@error_boundary
def render_about() -> None:
    """Render the About section with professional summary and credentials."""
    about_data = PORTFOLIO_DATA["about"]
    personal = PORTFOLIO_DATA["personal"]

    render_html('<div class="section-header">About Me</div>')
    render_html("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>Professional background, credentials, and developer setup.</p>")

    # Professional Summary — full width
    render_html(f"""
    <div class="glass-card" style="margin-bottom: 25px;">
        <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
            <span>{icon("target", 20)}</span> Professional Summary
        </h4>
        <p style="color: var(--text-color); font-size: 1.05rem; line-height: 1.6; margin: 0;">
            {about_data['summary']}
        </p>
    </div>
    """)

    # Details & Education — side by side
    e_col1, e_col2 = st.columns(2, gap="large")

    with e_col1:
        render_html(f"""
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>{icon("info", 20)}</span> Details & Credentials
            </h4>
            <div style="display: grid; gap: 15px;">
                <div>
                    <strong style="color: var(--text-color);">{icon("map-pin", 16)} Location:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">{personal['location']}</div>
                </div>
                <div>
                    <strong style="color: var(--text-color);">{icon("mail", 16)} Email:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">
                        <a href="mailto:{personal['email']}" style="color: var(--accent-color); text-decoration: none;">{personal['email']}</a>
                    </div>
                </div>
                <div>
                    <strong style="color: var(--text-color);">{icon("message-circle", 16)} Languages:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">{", ".join(about_data['languages'])}</div>
                </div>
            </div>
        </div>
        """)

    with e_col2:
        edu_html = ""
        for edu in about_data["education"]:
            edu_html += f"""
            <div style="margin-bottom: 10px;">
                <div style="font-weight: 600; color: var(--text-color);">{edu['degree']}</div>
                <div style="font-size: 0.9rem; color: var(--accent-color);">{edu['institution']}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">{edu['year']}</div>
            </div>
            """

        ws = about_data["workspace_info"]
        render_html(f"""
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>{icon("graduation-cap", 20)}</span> Education
            </h4>
            {edu_html}
            <div style="margin-top: 20px; padding-top: 18px; border-top: 1px solid var(--border-color);">
                <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1rem; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                    <span>{icon("monitor", 16)}</span> Workspace
                </h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 0.9rem;">
                    <div>
                        <div style="color: var(--text-muted); font-size: 0.8rem;">OS</div>
                        <div style="font-weight: 600; color: var(--text-color);">{ws['os']}</div>
                    </div>
                    <div>
                        <div style="color: var(--text-muted); font-size: 0.8rem;">Editor</div>
                        <div style="font-weight: 600; color: var(--text-color);">{ws['editor']}</div>
                    </div>
                    <div>
                        <div style="color: var(--text-muted); font-size: 0.8rem;">Terminal</div>
                        <div style="font-weight: 600; color: var(--text-color);">{ws['terminal']}</div>
                    </div>

                </div>
            </div>
        </div>
        """)


