# -*- coding: utf-8 -*-
import functools
import json
import traceback
from datetime import datetime, timezone
import streamlit as st
import requests
import os
from typing import Callable, Any, Optional, Dict, List

# Dynamic CSS Theme Overrides
DARK_VARS = """
:root {
    --bg-color: #081018;
    --card-bg: rgba(16, 24, 38, 0.75);
    --surface-subtle: rgba(255, 255, 255, 0.02);
    --border-color: rgba(79, 124, 255, 0.15);
    --accent-color: #4F7CFF;
    --accent-glow: rgba(79, 124, 255, 0.25);
    --accent-secondary: #00D4FF;
    --text-color: #F5F7FA;
    --text-muted: #A0AEC0;
    --shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    --sidebar-bg: #050a10;
    --glass-shine: rgba(255,255,255,0.1);
    --btn-shine: rgba(255,255,255,0.2);
    --skeleton-shine: rgba(255,255,255,0.08);
    --track-bg: rgba(255,255,255,0.08);
    --color-success: #00d464;
    --color-warning: #f59e0b;
    --color-error: #ef4444;
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
    --shadow-glow: 0 0 20px rgba(79, 124, 255, 0.3);
}
"""

LIGHT_VARS = """
:root {
    --bg-color: #F5F7FA;
    --card-bg: rgba(255, 255, 255, 0.92);
    --surface-subtle: rgba(79, 124, 255, 0.06);
    --border-color: rgba(79, 124, 255, 0.18);
    --accent-color: #4F7CFF;
    --accent-glow: rgba(79, 124, 255, 0.15);
    --accent-secondary: #00D4FF;
    --text-color: #111827;
    --text-muted: #6B7280;
    --shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.06);
    --sidebar-bg: #EAEFF5;
    --glass-shine: rgba(0,0,0,0.05);
    --btn-shine: rgba(0,0,0,0.08);
    --skeleton-shine: rgba(0,0,0,0.06);
    --track-bg: rgba(0,0,0,0.08);
    --color-success: #00d464;
    --color-warning: #f59e0b;
    --color-error: #ef4444;
    --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.03);
    --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.06);
    --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
    --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.1);
    --shadow-glow: 0 0 20px rgba(79, 124, 255, 0.15);
}
"""

@st.cache_data(show_spinner=False)
def _read_main_css() -> str:
    """Read main.css from disk (cached)."""
    css_path = os.path.join(os.path.dirname(__file__), "..", "styles", "main.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


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

    # Load Google Font asynchronously (avoids render-blocking @import)
    st.html(
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?'
        'family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
    )

    # Inject variables + main.css stylesheet (cached read)
    main_css = _read_main_css()
    st.markdown(f"<style>{theme_css}\n{main_css}</style>", unsafe_allow_html=True)


def render_html(html: str, *, height: Optional[int] = None) -> None:
    """Render raw HTML reliably (avoids escaped tags in markdown blocks)."""
    kwargs: Dict[str, Any] = {}
    if height is not None:
        kwargs["height"] = height
    st.html(html, **kwargs)


def plotly_polar_theme(theme: str) -> Dict[str, str]:
    """Grid and label colors for Plotly polar charts."""
    if theme == "dark":
        return {"grid": "rgba(160, 174, 192, 0.12)", "text": "#A0AEC0"}
    return {"grid": "rgba(107, 114, 128, 0.12)", "text": "#4B5563"}



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
        "scikitlearn": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/scikitlearn/scikitlearn-original.svg",
        "pandas": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg",
        "docker": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
        "git": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
        "linux": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg",
        "postgresql": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg",
        "vscode": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg",
    }
    key = name.lower().replace(" ", "").replace("5", "").replace("3", "").replace("&", "")
    return mapping.get(key, "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg")


@st.cache_data(ttl=600, show_spinner=False)
def github_last_active(username: str) -> str:
    """Return a human-readable string of when the user was last active on GitHub.

    Uses the public events endpoint. Returns empty string on failure.
    """
    url = f"https://api.github.com/users/{username}/events/public?per_page=1"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            events = r.json()
            if events:
                from datetime import datetime, timezone
                event_time = datetime.fromisoformat(events[0]["created_at"].replace("Z", "+00:00"))
                now = datetime.now(timezone.utc)
                diff = now - event_time
                mins = int(diff.total_seconds() / 60)
                if mins < 1:
                    return "just now"
                if mins < 60:
                    return f"{mins}m ago"
                hours = mins // 60
                if hours < 24:
                    return f"{hours}h ago"
                days = hours // 24
                return f"{days}d ago"
        return ""
    except Exception:
        return ""


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


@st.cache_data(ttl=300, show_spinner=False)
def load_articles(content_dir: str = "content") -> List[Dict[str, Any]]:
    """Load articles from markdown files with YAML frontmatter.

    Scans content_dir for .md files, parses frontmatter manually,
    and returns sorted list of article dicts.
    """
    import glob
    articles = []
    content_path = os.path.join(os.path.dirname(__file__), "..", content_dir)

    if not os.path.exists(content_path):
        return articles

    for filepath in sorted(glob.glob(os.path.join(content_path, "*.md"))):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if not content.startswith("---"):
                continue

            parts = content.split("---", 2)
            if len(parts) < 3:
                continue

            frontmatter = parts[1].strip()
            body = parts[2].strip()

            meta = {}
            for line in frontmatter.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    meta[key.strip()] = value.strip().strip('"').strip("'")

            word_count = len(body.split())
            reading_time = max(1, word_count // 200)

            articles.append({
                "title": meta.get("title", "Untitled"),
                "date": meta.get("date", ""),
                "category": meta.get("category", "General"),
                "excerpt": meta.get("excerpt", ""),
                "image": meta.get("image", ""),
                "read_time": f"{reading_time} min read",
                "content": body,
                "filename": os.path.basename(filepath),
            })
        except Exception:
            continue

    articles.sort(key=lambda x: x.get("date", ""), reverse=True)
    return articles


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
