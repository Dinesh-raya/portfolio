# -*- coding: utf-8 -*-
import streamlit as st
from utils.helpers import inject_theme_and_css, render_html
from data.portfolio_data import PORTFOLIO_DATA
from components.hero import render_hero
from components.about import render_about
from components.projects import render_projects
from components.skills import render_skills
from components.tech_stack import render_tech_stack
from components.experience import render_experience
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
    "Home", "About", "Projects", "Skills",
    "Tech Stack", "Experience", "Articles",
    "Playground", "Contact",
]

# Header with name, nav, and theme toggle
is_dark = st.session_state.theme == "dark"
toggle_icon = "☀️" if is_dark else "🌙"

render_html(f"""
<div class="top-header">
    <div class="top-header-left">
        <span class="top-logo">DR</span>
        <span class="top-name">{personal['name']}</span>
    </div>
    <div class="top-header-right">
        <span class="top-status"><span class="status-dot"></span> Available</span>
    </div>
</div>
""")

# Navigation tabs
selected = st.tabs(nav_items)

# Theme toggle in a small row above tabs
col_nav, col_toggle = st.columns([0.92, 0.08])
with col_toggle:
    if st.button(toggle_icon, key="theme_toggle", help="Toggle theme"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# Main Content Router (using tabs)
# ─────────────────────────────────────────────────────────────────────────────
# Add page content wrapper for staggered fade-in animations
st.markdown('<div class="page-content">', unsafe_allow_html=True)

with selected[0]:  # Home
    render_hero()

with selected[1]:  # About
    render_about()

with selected[2]:  # Projects
    render_projects()

with selected[3]:  # Skills
    render_skills()

with selected[4]:  # Tech Stack
    render_tech_stack()

with selected[5]:  # Experience
    render_experience()

with selected[6]:  # Articles
    render_articles()

with selected[7]:  # Playground
    render_playground()

with selected[8]:  # Contact
    render_contact()

st.markdown('</div>', unsafe_allow_html=True)

# ── Shared page footer ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="page-footer">
    <div style="margin-bottom: 10px;">
        <a href="{personal['github']}"   target="_blank">GitHub</a>
        &nbsp;·&nbsp;
        <a href="{personal['linkedin']}" target="_blank">LinkedIn</a>
        &nbsp;·&nbsp;
        <a href="mailto:{personal['email']}">Email</a>
    </div>
    <div>
        Crafted with ❤️ by <strong style="color:var(--accent-color);">Dinesh Raya</strong>
        &nbsp;·&nbsp; Built with
        <strong style="color:var(--accent-color);">Python &amp; Streamlit</strong>
        &nbsp;·&nbsp; © 2026
    </div>
</div>
""", unsafe_allow_html=True)
