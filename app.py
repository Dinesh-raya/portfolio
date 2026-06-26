# -*- coding: utf-8 -*-
import streamlit as st
from utils.helpers import inject_theme_and_css, render_html
from utils.icons import icon
from data.portfolio_data import PORTFOLIO_DATA
from components.hero import render_hero
from components.about import render_about
from components.projects import render_projects
from components.tech_stack import render_tech_stack
from components.articles import render_articles
from components.playground import render_playground
from components.contact import render_contact

# ─────────────────────────────────────────────────────────────────────────────
# Page Config  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dinesh Raya | AI Engineer Portfolio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Session-state defaults
# ─────────────────────────────────────────────────────────────────────────────
def initialize_session_state() -> None:
    """Initialize all session state variables with defaults.

    This ensures consistent state across the application and
    prevents KeyError exceptions from missing state variables.
    """
    defaults = {
        "theme": "dark",
        "current_page": "Home",
        "chat_history": [],
        "proj_filter": "All",
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


initialize_session_state()

# ─────────────────────────────────────────────────────────────────────────────
# Inject theme + CSS
# ─────────────────────────────────────────────────────────────────────────────
inject_theme_and_css()

# ─────────────────────────────────────────────────────────────────────────────
# Data shortcuts
# ─────────────────────────────────────────────────────────────────────────────
personal = PORTFOLIO_DATA["personal"]

# ─────────────────────────────────────────────────────────────────────────────
# Top Navigation Bar
# ─────────────────────────────────────────────────────────────────────────────
nav_items = [
    "Home", "About", "Projects",
    "Tech Stack", "Articles",
    "Playground", "Contact",
]

# Header with name, status, and theme toggle at top
is_dark = st.session_state.theme == "dark"
toggle_label = "☀️ Light" if is_dark else "🌙 Dark"
col_header, col_toggle = st.columns([0.88, 0.12], gap="small")
with col_header:
    render_html(f"""
    <div class="top-header">
        <div class="top-header-left">
            <span class="top-logo">DR</span>
            <span class="top-name">{personal['name']}</span>
        </div>
    </div>
    """)

with col_toggle:
    toggle_btn = st.button(
        toggle_label, key="theme_toggle",
        help="Switch between dark and light mode",
        use_container_width=True,
    )
    if toggle_btn:
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

# Navigation tabs
selected = st.tabs(nav_items)


# ─────────────────────────────────────────────────────────────────────────────
# Main Content Router (using tabs)
# ─────────────────────────────────────────────────────────────────────────────
# Add page content wrapper for staggered fade-in animations
render_html('<div class="page-content" id="main-content">')

with selected[0]:  # Home
    render_hero()

with selected[1]:  # About
    render_about()

with selected[2]:  # Projects
    render_projects()

with selected[3]:  # Tech Stack
    render_tech_stack()

with selected[4]:  # Articles
    render_articles()

with selected[5]:  # Playground
    render_playground()

with selected[6]:  # Contact
    render_contact()

render_html('</div>')

# ── Shared page footer ────────────────────────────────────────────────────────
render_html(f"""
<div class="page-footer">
    <div style="margin-bottom: 10px;">
        <a href="{personal['github']}"   target="_blank">GitHub</a>
        &nbsp;·&nbsp;
        <a href="{personal['linkedin']}" target="_blank">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="mailto:{personal['email']}">Email</a>
    </div>
    <div>
        Crafted with {icon("heart", 14)} by <strong style="color:var(--accent-color);">Dinesh Raya</strong>
        &nbsp;·&nbsp; Built with
        <strong style="color:var(--accent-color);">Python &amp; Streamlit</strong>
        &nbsp;·&nbsp; © 2026
    </div>
    <button onclick="window.scrollTo({{top:0,behavior:'smooth'}})"
            class="back-to-top" title="Back to top">{icon("arrow-up", 18)}</button>
</div>
""")


