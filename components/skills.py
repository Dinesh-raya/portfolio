# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html

@error_boundary
def render_skills() -> None:
    """Render the Skills section with skill matrix."""
    skills_data = PORTFOLIO_DATA["skills"]
    
    render_html('<div class="section-header">Skills & Competency</div>')
    render_html("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>Core competencies across AI, software engineering, and data disciplines.</p>")
    
    for category in skills_data["categories"]:
            pills = "".join([f'<span class="tech-tag" style="font-size: 0.85rem; padding: 6px 12px; margin-bottom: 8px;">{item}</span>' for item in category["items"]])
            render_html(f"""
            <div class="glass-card" style="margin-bottom: 20px;">
                <h5 style="color: var(--accent-color); font-weight: 700; font-size: 1.15rem; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                    <span>📂</span> {category['title']}
                </h5>
                <div style="display: flex; flex-wrap: wrap;">
                    {pills}
                </div>
            </div>
            """)
