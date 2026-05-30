# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu
from utils.helpers import inject_theme_and_css
from data.portfolio_data import PORTFOLIO_DATA

# ─────────────────────────────────────────────────────────────────────────────
# Page Config  (must be the very first Streamlit call)
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dinesh Raya | AI Engineer Portfolio",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
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
# Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:

    # ── Logo / identity block ─────────────────────────────────────────────────
    st.markdown(f"""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <!-- Monogram badge -->
        <div style="
            width: 64px; height: 64px; border-radius: 16px; margin: 0 auto 12px auto;
            background: linear-gradient(135deg, #4F7CFF, #00D4FF);
            display: flex; align-items: center; justify-content: center;
            font-size: 1.6rem; font-weight: 800; color: white;
            box-shadow: 0 4px 20px rgba(79,124,255,0.35);
        ">DR</div>

        <div style="font-size: 1.15rem; font-weight: 700; color: var(--text-color);">
            {personal['name']}
        </div>
        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 4px; line-height: 1.4;">
            AI Enthusiast&nbsp;&bull;&nbsp;Developer&nbsp;&bull;&nbsp;Problem Solver
        </div>
    </div>

    <hr style="border: none; border-top: 1px solid var(--border-color); margin: 6px 0 14px 0;" />
    """, unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────────────────
    nav_icons = [
        "house-fill", "person-fill", "code-slash", "stars",
        "layers-fill", "clock-history", "journal-text",
        "controller", "envelope-fill",
    ]
    nav_items = [
        "Home", "About", "Projects", "Skills",
        "Tech Stack", "Experience", "Articles",
        "Playground", "Contact",
    ]

    selected = option_menu(
        menu_title=None,
        options=nav_items,
        icons=nav_icons,
        menu_icon="cast",
        default_index=nav_items.index(st.session_state.current_page)
                      if st.session_state.current_page in nav_items else 0,
        styles={
            "container":        {"padding": "0", "background-color": "transparent"},
            "icon":             {"color": "#4F7CFF", "font-size": "14px"},
            "nav-link":         {
                "font-size": "13px", "font-weight": "500",
                "color": "var(--text-muted)",
                "border-radius": "8px", "margin": "2px 0",
            },
            "nav-link-selected": {
                "background": "rgba(79,124,255,0.12)",
                "color": "#4F7CFF",
                "font-weight": "700",
            },
        },
        key="sidebar_nav",
    )
    st.session_state.current_page = selected

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # ── Theme Toggle ──────────────────────────────────────────────────────────
    is_dark = st.session_state.theme == "dark"
    toggle_label = "☀️  Switch to Light Mode" if is_dark else "🌙  Switch to Dark Mode"
    if st.button(toggle_label, use_container_width=True, key="theme_toggle"):
        st.session_state.theme = "light" if is_dark else "dark"
        st.rerun()

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # ── Social Icons ──────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 14px; flex-wrap: wrap; padding: 6px 0;">
        <a href="{personal['github']}"   target="_blank" title="GitHub"
           style="color: var(--text-muted); text-decoration: none; font-size: 1.3rem;
                  transition: color .2s;"
           onmouseover="this.style.color='#4F7CFF'"
           onmouseout="this.style.color='var(--text-muted)'">
           𝗚𝗛
        </a>
        <a href="{personal['linkedin']}" target="_blank" title="LinkedIn"
           style="color: var(--text-muted); text-decoration: none; font-size: 1.3rem;"
           onmouseover="this.style.color='#0A66C2'"
           onmouseout="this.style.color='var(--text-muted)'">
           in
        </a>
        <a href="mailto:{personal['email']}" title="Email"
           style="color: var(--text-muted); text-decoration: none; font-size: 1.3rem;"
           onmouseover="this.style.color='#4F7CFF'"
           onmouseout="this.style.color='var(--text-muted)'">
           ✉
        </a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    # ── Collaboration CTA ─────────────────────────────────────────────────────
    if st.button("🤝  Let's Collaborate", use_container_width=True, type="primary", key="collab_btn"):
        st.session_state.current_page = "Contact"
        st.rerun()

    # ── Footer ────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="text-align: center; margin-top: 24px; font-size: 0.72rem; color: var(--text-muted);">
        © 2026 Dinesh Raya<br>Built with ❤️ & Streamlit
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Main Content Router
# ─────────────────────────────────────────────────────────────────────────────
page = st.session_state.current_page

# Page breadcrumb / title strip
page_icons = {
    "Home": "🏠", "About": "👤", "Projects": "⚡", "Skills": "🌟",
    "Tech Stack": "🧩", "Experience": "🕐", "Articles": "📝",
    "Playground": "🎮", "Contact": "✉️",
}
if page != "Home":
    st.markdown(
        f"<p style='color:var(--text-muted); font-size:0.82rem; margin-bottom:6px; "
        f"text-transform:uppercase; letter-spacing:0.08em; font-weight:600;'>"
        f"Portfolio &rsaquo; {page}</p>",
        unsafe_allow_html=True,
    )

# Add page content wrapper for staggered fade-in animations
st.markdown('<div class="page-content">', unsafe_allow_html=True)

if page == "Home":
    from components.hero import render_hero
    render_hero()

elif page == "About":
    from components.about import render_about
    render_about()

elif page == "Projects":
    from components.projects import render_projects
    render_projects()

elif page == "Skills":
    from components.skills import render_skills
    render_skills()

elif page == "Tech Stack":
    from components.tech_stack import render_tech_stack
    render_tech_stack()

elif page == "Experience":
    from components.experience import render_experience
    render_experience()

elif page == "Articles":
    from components.articles import render_articles
    render_articles()

elif page == "Playground":
    from components.playground import render_playground
    render_playground()

elif page == "Contact":
    from components.contact import render_contact
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
