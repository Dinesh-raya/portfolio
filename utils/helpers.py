# -*- coding: utf-8 -*-
import functools
import traceback
import streamlit as st
import requests
import os
from typing import Callable, Any, Optional, Dict, List

# Dynamic CSS Theme Overrides
DARK_VARS = """
:root {
    --bg-color: #081018;
    --card-bg: rgba(16, 24, 38, 0.75);
    --border-color: rgba(79, 124, 255, 0.15);
    --accent-color: #4F7CFF;
    --accent-glow: rgba(79, 124, 255, 0.25);
    --accent-secondary: #00D4FF;
    --text-color: #F5F7FA;
    --text-muted: #A0AEC0;
    --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    --sidebar-bg: #050a10;
}
"""

LIGHT_VARS = """
:root {
    --bg-color: #F5F7FA;
    --card-bg: rgba(255, 255, 255, 0.75);
    --border-color: rgba(79, 124, 255, 0.1);
    --accent-color: #4F7CFF;
    --accent-glow: rgba(79, 124, 255, 0.15);
    --accent-secondary: #00D4FF;
    --text-color: #111827;
    --text-muted: #6B7280;
    --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.06);
    --sidebar-bg: #EAEFF5;
}
"""

def inject_theme_and_css() -> None:
    """Inject custom CSS variables depending on active theme and load main.css stylesheet.

    Reads the theme from st.session_state.theme ('dark' or 'light'),
    selects appropriate CSS variables, and injects them along with
    the main.css file contents into the Streamlit page.
    """
    # Ensure theme exists in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
        
    theme_css = DARK_VARS if st.session_state.theme == "dark" else LIGHT_VARS
    
    # Read main stylesheet
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "main.css")
    main_css = ""
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            main_css = f.read()
            
    # Inject variables + main.css stylesheet
    st.markdown(f"<style>{theme_css}\n{main_css}</style>", unsafe_allow_html=True)


def load_lottie_url(url: str) -> Optional[Dict[str, Any]]:
    """Load a Lottie animation from a URL.

    Args:
        url: URL to the Lottie animation JSON file.

    Returns:
        Parsed JSON dict if successful, None on failure.
    """
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None


def get_tech_icon_url(name: str) -> str:
    """Return the official Devicon SVG URL for a given technology.

    Args:
        name: Technology name (e.g., 'python', 'javascript').

    Returns:
        URL string to the technology's SVG icon, or a Python icon as fallback.
    """
    mapping = {
        "python": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "javascript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
        "typescript": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
        "html": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg",
        "css": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
        "streamlit": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/streamlit/streamlit-original.svg",
        "fastapi": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg",
        "pytorch": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytorch/pytorch-original.svg",
        "scikitlearn": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg", # fallback
        "pandas": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg",
        "docker": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
        "git": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
        "linux": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg",
        "postgresql": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg",
        "vscode": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg",
    }
    key = name.lower().replace(" ", "").replace("5", "").replace("3", "").replace("&", "")
    return mapping.get(key, "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg")


@st.cache_data(ttl=3600)  # cache results for 1 hour to prevent API rate limiting
def github_fetch_repos(username: str) -> List[Dict[str, Any]]:
    """Fetch public repositories metadata from GitHub API.

    Args:
        username: GitHub username to fetch repos for.

    Returns:
        List of repository dicts sorted by stargazers_count descending.
        Returns empty list on failure.
    """
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            repos = r.json()
            # Sort by stargazers count desc
            repos = sorted(repos, key=lambda x: x.get("stargazers_count", 0), reverse=True)
            return repos
    except Exception:
        pass
    return []


def error_boundary(func: Callable) -> Callable:
    """Decorator that wraps component render functions with error handling.

    Catches exceptions and displays a user-friendly error message
    instead of crashing the entire app.

    Args:
        func: The render function to wrap.

    Returns:
        Wrapped function with try/except error handling.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error("⚠️ Something went wrong loading this section. Please try refreshing the page.")
            with st.expander("Technical Details"):
                st.code(traceback.format_exc())
            return None
    return wrapper
