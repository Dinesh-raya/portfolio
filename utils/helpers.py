# -*- coding: utf-8 -*-
import functools
import json
import traceback
from datetime import datetime, timezone
import streamlit as st
import requests
import os
from typing import Callable, Any, Optional, Dict, List, Tuple

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


def render_html(html: str, *, height: Optional[int] = None) -> None:
    """Render raw HTML reliably (avoids escaped tags in markdown blocks)."""
    kwargs: Dict[str, Any] = {}
    if height is not None:
        kwargs["height"] = height
    st.html(html, **kwargs)


def get_formspree_form_id() -> Optional[str]:
    """Return Formspree form ID from Streamlit secrets, if configured."""
    try:
        form_id = st.secrets.get("formspree", {}).get("form_id")
        if form_id and str(form_id).strip() and "your_formspree" not in str(form_id).lower():
            return str(form_id).strip()
    except Exception:
        pass
    return None


def _save_message_local(
    name: str,
    email: str,
    subject: str,
    message: str,
    source: str,
) -> None:
    os.makedirs("assets", exist_ok=True)
    msg_path = os.path.join("assets", "messages.json")
    messages: List[Dict[str, Any]] = []
    if os.path.exists(msg_path):
        with open(msg_path, "r", encoding="utf-8") as f:
            try:
                messages = json.load(f)
            except (json.JSONDecodeError, OSError):
                messages = []
    messages.append(
        {
            "name": name,
            "email": email,
            "subject": subject,
            "message": message,
            "source": source,
            "at": datetime.now(timezone.utc).isoformat(),
        }
    )
    with open(msg_path, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2)


def send_contact_form(
    name: str,
    email: str,
    subject: str,
    message: str,
    *,
    source: str = "contact",
) -> Tuple[bool, str]:
    """Deliver contact form: Formspree (production) or local JSON (dev).

    Returns:
        (success, user_facing_message)
    """
    name = name.strip()
    email = email.strip()
    subject = (subject or "Portfolio contact").strip()
    message = message.strip()

    if not name:
        return False, "Please enter your name."
    if not email or "@" not in email:
        return False, "Please enter a valid email address."
    if not message:
        return False, "Please enter a message."
    if len(message) < 20:
        return False, "Message should be at least 20 characters."

    form_id = get_formspree_form_id()
    if form_id:
        try:
            payload = {
                "name": name,
                "email": email,
                "_subject": subject or f"Portfolio message from {name}",
                "message": message,
                "source": source,
            }
            r = requests.post(
                f"https://formspree.io/f/{form_id}",
                json=payload,
                headers={"Accept": "application/json"},
                timeout=10,
            )
            if r.status_code in (200, 201, 302):
                return True, f"Thanks {name}! Your message was sent. I'll get back to you soon."
            return False, "Could not send your message right now. Please email me directly."
        except requests.RequestException:
            return False, "Network error while sending. Please try again or email me directly."

    if os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT") == "cloud":
        return (
            False,
            "Contact form is not configured for production. Add Formspree secrets — see README.",
        )

    try:
        _save_message_local(name, email, subject, message, source)
        return True, f"Thanks {name}! Your message was saved (local dev). I'll get back to you soon."
    except OSError:
        return (
            False,
            "Contact form is not configured. Add Formspree secrets — see README.",
        )


def plotly_polar_theme(theme: str) -> Dict[str, str]:
    """Grid and label colors for Plotly polar charts."""
    if theme == "dark":
        return {"grid": "rgba(160, 174, 192, 0.12)", "text": "#A0AEC0"}
    return {"grid": "rgba(107, 114, 128, 0.12)", "text": "#4B5563"}


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
