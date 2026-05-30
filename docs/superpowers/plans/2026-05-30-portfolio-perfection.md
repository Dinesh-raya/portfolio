# Portfolio Perfection Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the existing Streamlit portfolio into a premium, polished, and performant application with smooth animations, excellent mobile experience, and clean code architecture.

**Architecture:** Parallel improvement tracks working on CSS design system, Python code quality, animations, and mobile responsiveness simultaneously. Each track is independent and can be executed in parallel.

**Tech Stack:** Python, Streamlit, CSS3 (custom properties, animations, glassmorphism), Plotly

---

## File Structure

### Files to Modify

| File | Responsibility | Track |
|------|---------------|-------|
| `styles/main.css` | Design tokens, animations, responsive breakpoints, glassmorphism | Visual + Animations + Mobile |
| `app.py` | Error handling, state management, page transitions | Code Quality |
| `utils/helpers.py` | Type hints, error handling, utility functions | Code Quality |
| `components/hero.py` | Hero section improvements | Visual + Mobile |
| `components/about.py` | About section improvements | Visual + Mobile |
| `components/projects.py` | Projects section improvements | Visual + Mobile |
| `components/skills.py` | Skills section improvements | Visual + Mobile |
| `components/tech_stack.py` | Tech stack section improvements | Visual + Mobile |
| `components/experience.py` | Experience section improvements | Visual + Mobile |
| `components/articles.py` | Articles section improvements | Visual + Mobile |
| `components/playground.py` | Playground section improvements | Visual + Mobile |
| `components/contact.py` | Contact section improvements | Visual + Mobile |
| `.streamlit/config.toml` | Theme configuration | Visual |

---

## Track A: Visual Polish & Design System

### Task A1: Design Tokens & CSS Variables

**Files:**
- Modify: `styles/main.css:1-50`

- [ ] **Step 1: Add design token CSS variables**

Add the following CSS variables to the `:root` selector in `styles/main.css`:

```css
/* Design Tokens - Spacing */
--space-xs: 4px;
--space-sm: 8px;
--space-md: 16px;
--space-lg: 24px;
--space-xl: 32px;
--space-2xl: 48px;
--space-3xl: 64px;

/* Design Tokens - Border Radius */
--radius-sm: 8px;
--radius-md: 12px;
--radius-lg: 16px;
--radius-xl: 24px;
--radius-full: 9999px;

/* Design Tokens - Typography Scale */
--font-size-xs: 0.75rem;
--font-size-sm: 0.875rem;
--font-size-md: 1rem;
--font-size-lg: 1.125rem;
--font-size-xl: 1.25rem;
--font-size-2xl: 1.5rem;
--font-size-3xl: 2rem;
--font-size-4xl: 2.5rem;
--font-size-5xl: 3rem;

/* Design Tokens - Font Weights */
--font-light: 300;
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
--font-extrabold: 800;

/* Design Tokens - Line Heights */
--leading-tight: 1.1;
--leading-snug: 1.3;
--leading-normal: 1.5;
--leading-relaxed: 1.65;

/* Design Tokens - Shadows */
--shadow-xs: 0 1px 2px rgba(0,0,0,0.05);
--shadow-sm: 0 2px 8px rgba(0,0,0,0.1);
--shadow-md: 0 4px 16px rgba(0,0,0,0.15);
--shadow-lg: 0 8px 32px rgba(0,0,0,0.2);
--shadow-xl: 0 16px 48px rgba(0,0,0,0.25);
--shadow-glow: 0 0 20px rgba(79,124,255,0.3);
--shadow-glow-lg: 0 0 40px rgba(79,124,255,0.4);

/* Design Tokens - Transitions */
--transition-fast: 150ms ease;
--transition-base: 250ms ease;
--transition-slow: 400ms ease;
--transition-spring: 500ms cubic-bezier(0.34, 1.56, 0.64, 1);
```

- [ ] **Step 2: Update existing CSS to use design tokens**

Replace hardcoded values in `styles/main.css` with the new design tokens. Example:

```css
/* Before */
.glass-card {
    padding: 24px !important;
    border-radius: 16px !important;
}

/* After */
.glass-card {
    padding: var(--space-lg) !important;
    border-radius: var(--radius-lg) !important;
}
```

- [ ] **Step 3: Verify visual consistency**

Run the Streamlit app and verify that the design tokens are applied correctly:
```bash
streamlit run app.py
```

Expected: No visual regressions, all spacing and sizing remains consistent.

- [ ] **Step 4: Commit design tokens**

```bash
git add styles/main.css
git commit -m "feat: add design token system with CSS custom properties"
```

---

### Task A2: Glassmorphism Upgrade

**Files:**
- Modify: `styles/main.css:26-42`

- [ ] **Step 1: Upgrade glass-card styles**

Replace the existing `.glass-card` styles with enhanced glassmorphism:

```css
.glass-card {
    background: var(--card-bg) !important;
    backdrop-filter: blur(20px) saturate(180%) !important;
    -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: var(--radius-lg) !important;
    padding: var(--space-lg) !important;
    box-shadow: var(--shadow-md) !important;
    transition: all var(--transition-base) cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    margin-bottom: var(--space-lg);
    position: relative;
    overflow: hidden;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255,255,255,0.1), 
        transparent
    );
    pointer-events: none;
}

.glass-card:hover {
    transform: translateY(-4px) scale(1.01);
    border-color: rgba(79, 124, 255, 0.4) !important;
    box-shadow: 
        var(--shadow-lg),
        var(--shadow-glow) !important;
}
```

- [ ] **Step 2: Add glass-card variants**

Add specialized card variants:

```css
.glass-card-sm {
    padding: var(--space-md) !important;
    border-radius: var(--radius-md) !important;
}

.glass-card-lg {
    padding: var(--space-xl) !important;
    border-radius: var(--radius-xl) !important;
}

.glass-card-accent {
    border-left: 3px solid var(--accent-color) !important;
}
```

- [ ] **Step 3: Verify glassmorphism effect**

Run the app and check that cards have:
- Visible blur effect on background
- Subtle top border highlight
- Smooth hover animation with glow
- No performance issues

- [ ] **Step 4: Commit glassmorphism upgrade**

```bash
git add styles/main.css
git commit -m "feat: upgrade glassmorphism with enhanced blur and hover effects"
```

---

### Task A3: Typography Improvements

**Files:**
- Modify: `styles/main.css:1-10`
- Modify: `styles/main.css:76-91`

- [ ] **Step 1: Improve font loading**

Update the font import and base styles:

```css
/* Load custom Outfit font from Google Fonts - optimized */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

/* Apply font with proper fallbacks */
* {
    font-family: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}
```

- [ ] **Step 2: Update typography classes**

Replace existing typography styles with design token-based versions:

```css
.gradient-text {
    background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: var(--font-extrabold);
    line-height: var(--leading-tight);
}

.section-header {
    font-size: var(--font-size-3xl);
    font-weight: var(--font-bold);
    margin-bottom: var(--space-sm);
    border-bottom: 2px solid var(--border-color);
    padding-bottom: var(--space-sm);
    display: inline-block;
    letter-spacing: -0.02em;
}

.section-subtitle {
    font-size: var(--font-size-lg);
    color: var(--text-muted);
    margin-bottom: var(--space-xl);
    line-height: var(--leading-relaxed);
}
```

- [ ] **Step 3: Add responsive typography**

```css
@media (max-width: 768px) {
    .section-header {
        font-size: var(--font-size-2xl) !important;
    }
    .section-subtitle {
        font-size: var(--font-size-md) !important;
    }
}

@media (max-width: 480px) {
    .section-header {
        font-size: var(--font-size-xl) !important;
    }
}
```

- [ ] **Step 4: Verify typography**

Check that:
- Font loads correctly
- Heading hierarchy is clear
- Text is readable on all screen sizes
- Gradient text renders properly

- [ ] **Step 5: Commit typography improvements**

```bash
git add styles/main.css
git commit -m "feat: improve typography with design tokens and responsive scaling"
```

---

### Task A4: Button & Link Styles

**Files:**
- Modify: `styles/main.css:93-133`

- [ ] **Step 1: Upgrade button styles**

Replace existing button styles:

```css
.custom-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-sm);
    background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary));
    color: white !important;
    padding: var(--space-sm) var(--space-lg);
    border-radius: var(--radius-md);
    font-weight: var(--font-semibold);
    font-size: var(--font-size-sm);
    text-decoration: none !important;
    transition: all var(--transition-base) !important;
    border: none;
    box-shadow: var(--shadow-sm);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}

.custom-btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        90deg,
        transparent,
        rgba(255,255,255,0.2),
        transparent
    );
    transition: left var(--transition-slow);
}

.custom-btn:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md), var(--shadow-glow);
}

.custom-btn:hover::before {
    left: 100%;
}

.custom-btn:active {
    transform: translateY(0);
    box-shadow: var(--shadow-xs);
}

.custom-btn-outline {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-sm);
    background: transparent;
    color: var(--text-color) !important;
    padding: var(--space-sm) var(--space-lg);
    border-radius: var(--radius-md);
    font-weight: var(--font-semibold);
    font-size: var(--font-size-sm);
    text-decoration: none !important;
    transition: all var(--transition-base) !important;
    border: 2px solid var(--border-color);
    cursor: pointer;
}

.custom-btn-outline:hover {
    border-color: var(--accent-color);
    background: rgba(79, 124, 255, 0.05);
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}
```

- [ ] **Step 2: Add Streamlit button overrides**

```css
.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: var(--font-semibold) !important;
    font-family: 'Outfit', sans-serif !important;
    transition: all var(--transition-base) !important;
    letter-spacing: 0.01em !important;
    padding: var(--space-sm) var(--space-lg) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-md), var(--shadow-glow) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent-color), var(--accent-secondary)) !important;
    border: none !important;
    color: white !important;
}
```

- [ ] **Step 3: Verify button interactions**

Check that:
- Buttons have smooth hover animations
- Click feedback works correctly
- Gradient shimmer effect is visible
- Outline buttons have proper border transitions

- [ ] **Step 4: Commit button improvements**

```bash
git add styles/main.css
git commit -m "feat: upgrade button styles with shimmer effects and better interactions"
```

---

## Track B: Code Quality & Foundation

### Task B1: Error Handling Wrapper

**Files:**
- Modify: `utils/helpers.py:1-10`
- Modify: `components/hero.py:1-10`
- Modify: `components/about.py:1-10`
- Modify: `components/projects.py:1-10`
- Modify: `components/skills.py:1-10`
- Modify: `components/tech_stack.py:1-10`
- Modify: `components/experience.py:1-10`
- Modify: `components/articles.py:1-10`
- Modify: `components/playground.py:1-10`
- Modify: `components/contact.py:1-10`

- [ ] **Step 1: Create error boundary decorator in helpers.py**

Add the following to `utils/helpers.py`:

```python
import functools
import traceback
import streamlit as st
from typing import Callable, Any

def error_boundary(func: Callable) -> Callable:
    """Decorator that wraps component render functions with error handling.
    
    Catches exceptions and displays a user-friendly error message
    instead of crashing the entire app.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"⚠️ Something went wrong loading this section. Please try refreshing the page.")
            with st.expander("Technical Details"):
                st.code(traceback.format_exc())
            return None
    return wrapper
```

- [ ] **Step 2: Apply error boundary to hero.py**

Update `components/hero.py`:

```python
# -*- coding: utf-8 -*-
import streamlit as st
import os
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary

@error_boundary
def render_hero():
    personal = PORTFOLIO_DATA["personal"]
    stats    = PORTFOLIO_DATA["stats"]
    theme    = st.session_state.get("theme", "dark")
    # ... rest of the function remains the same
```

- [ ] **Step 3: Apply error boundary to all components**

Apply the same `@error_boundary` decorator to all component render functions:
- `about.py`: `render_about()`
- `projects.py`: `render_projects()`
- `skills.py`: `render_skills()`
- `tech_stack.py`: `render_tech_stack()`
- `experience.py`: `render_experience()`
- `articles.py`: `render_articles()`
- `playground.py`: `render_playground()`
- `contact.py`: `render_contact()`

- [ ] **Step 4: Test error handling**

Intentionally cause an error (e.g., access a non-existent key) and verify:
- Error message displays gracefully
- Other sections continue to work
- Technical details are available in expander

- [ ] **Step 5: Commit error handling**

```bash
git add utils/helpers.py components/*.py
git commit -m "feat: add error boundary decorator to all components"
```

---

### Task B2: Type Hints & Docstrings

**Files:**
- Modify: `utils/helpers.py`
- Modify: `components/*.py`

- [ ] **Step 1: Add type hints to helpers.py**

Update all functions in `utils/helpers.py` with proper type hints:

```python
from typing import Optional, Dict, List, Any
import streamlit as st

def inject_theme_and_css() -> None:
    """Injects custom CSS variables depending on active theme + the main.css file."""
    # ... implementation

def load_lottie_url(url: str) -> Optional[Dict[str, Any]]:
    """Loads a lottie animation from url.
    
    Args:
        url: URL to the Lottie animation JSON
        
    Returns:
        Parsed JSON dict if successful, None otherwise
    """
    # ... implementation

def get_tech_icon_url(name: str) -> str:
    """Returns official Devicon SVG URLs for technologies, with fallbacks.
    
    Args:
        name: Technology name (e.g., 'python', 'javascript')
        
    Returns:
        URL string to the technology's SVG icon
    """
    # ... implementation

@st.cache_data(ttl=3600)
def github_fetch_repos(username: str) -> List[Dict[str, Any]]:
    """Fetches public repositories metadata from GitHub API.
    
    Args:
        username: GitHub username to fetch repos for
        
    Returns:
        List of repository dicts sorted by stargazers_count desc
    """
    # ... implementation

def error_boundary(func: Callable) -> Callable:
    """Decorator that wraps component render functions with error handling.
    
    Args:
        func: The render function to wrap
        
    Returns:
        Wrapped function with error handling
    """
    # ... implementation
```

- [ ] **Step 2: Add type hints to component functions**

Add return type hints to all component render functions:

```python
def render_hero() -> None:
    """Render the Hero/Home section with animated stats and CTAs."""
    # ...

def render_about() -> None:
    """Render the About section with professional summary and credentials."""
    # ...

def render_projects() -> None:
    """Render the Projects section with filtering and GitHub integration."""
    # ...

def render_skills() -> None:
    """Render the Skills section with radar chart and skill matrix."""
    # ...

def render_tech_stack() -> None:
    """Render the Tech Stack section with technology icons."""
    # ...

def render_experience() -> None:
    """Render the Experience section with timeline layout."""
    # ...

def render_articles() -> None:
    """Render the Articles section with category cards."""
    # ...

def render_playground() -> None:
    """Render the Interactive Playground with AI tools."""
    # ...

def render_contact() -> None:
    """Render the Contact section with form and details."""
    # ...
```

- [ ] **Step 3: Verify no syntax errors**

Run Python syntax check:
```bash
python -m py_compile utils/helpers.py
python -m py_compile components/*.py
```

Expected: No errors

- [ ] **Step 4: Commit type hints**

```bash
git add utils/helpers.py components/*.py
git commit -m "feat: add type hints and docstrings to all functions"
```

---

### Task B3: Session State Management

**Files:**
- Modify: `app.py:19-25`

- [ ] **Step 1: Create session state initialization function**

Add to `app.py`:

```python
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
```

- [ ] **Step 2: Replace inline initialization**

Replace the existing inline initialization in `app.py`:

```python
# Before
if "theme"        not in st.session_state:
    st.session_state.theme = "dark"
if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# After
initialize_session_state()
```

- [ ] **Step 3: Verify state management**

Test that:
- Theme toggle works correctly
- Page navigation maintains state
- Chat history persists across reruns
- Project filter works correctly

- [ ] **Step 4: Commit state management**

```bash
git add app.py
git commit -m "refactor: centralize session state initialization"
```

---

## Track C: Animations & Transitions

### Task C1: Page Transition Animations

**Files:**
- Modify: `styles/main.css`
- Modify: `app.py`

- [ ] **Step 1: Add page transition CSS**

Add to `styles/main.css`:

```css
/* Page Transitions */
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes fadeInUp {
    from { 
        opacity: 0; 
        transform: translateY(20px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

@keyframes fadeInDown {
    from { 
        opacity: 0; 
        transform: translateY(-20px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}

@keyframes fadeInLeft {
    from { 
        opacity: 0; 
        transform: translateX(-20px); 
    }
    to { 
        opacity: 1; 
        transform: translateX(0); 
    }
}

@keyframes fadeInRight {
    from { 
        opacity: 0; 
        transform: translateX(20px); 
    }
    to { 
        opacity: 1; 
        transform: translateX(0); 
    }
}

@keyframes scaleIn {
    from { 
        opacity: 0; 
        transform: scale(0.95); 
    }
    to { 
        opacity: 1; 
        transform: scale(1); 
    }
}

/* Animation Classes */
.animate-fade-in {
    animation: fadeIn var(--transition-slow) ease forwards;
}

.animate-fade-in-up {
    animation: fadeInUp var(--transition-slow) ease forwards;
}

.animate-fade-in-down {
    animation: fadeInDown var(--transition-slow) ease forwards;
}

.animate-fade-in-left {
    animation: fadeInLeft var(--transition-slow) ease forwards;
}

.animate-fade-in-right {
    animation: fadeInRight var(--transition-slow) ease forwards;
}

.animate-scale-in {
    animation: scaleIn var(--transition-slow) ease forwards;
}

/* Stagger delays */
.delay-100 { animation-delay: 100ms; }
.delay-200 { animation-delay: 200ms; }
.delay-300 { animation-delay: 300ms; }
.delay-400 { animation-delay: 400ms; }
.delay-500 { animation-delay: 500ms; }
```

- [ ] **Step 2: Add page container animation**

Add wrapper class for page content:

```css
/* Page Content Wrapper */
.page-content {
    animation: fadeIn 300ms ease forwards;
}

.page-content > * {
    opacity: 0;
    animation: fadeInUp 400ms ease forwards;
}

.page-content > *:nth-child(1) { animation-delay: 0ms; }
.page-content > *:nth-child(2) { animation-delay: 50ms; }
.page-content > *:nth-child(3) { animation-delay: 100ms; }
.page-content > *:nth-child(4) { animation-delay: 150ms; }
.page-content > *:nth-child(5) { animation-delay: 200ms; }
```

- [ ] **Step 3: Apply page transitions in app.py**

Wrap page content in animated container:

```python
# In the main content router section
if page != "Home":
    st.markdown(
        f"<p style='color:var(--text-muted); font-size:0.82rem; margin-bottom:6px; "
        f"text-transform:uppercase; letter-spacing:0.08em; font-weight:600;'>"
        f"Portfolio &rsaquo; {page}</p>",
        unsafe_allow_html=True,
    )

# Add page content wrapper
st.markdown('<div class="page-content">', unsafe_allow_html=True)

# ... page routing ...

st.markdown('</div>', unsafe_allow_html=True)
```

- [ ] **Step 4: Verify page transitions**

Navigate between pages and verify:
- Smooth fade-in effect
- Content appears with stagger
- No layout shifts during animation
- Animation completes properly

- [ ] **Step 5: Commit page transitions**

```bash
git add styles/main.css app.py
git commit -m "feat: add page transition animations with staggered fade-in"
```

---

### Task C2: Scroll-Triggered Animations

**Files:**
- Modify: `styles/main.css`
- Modify: `utils/helpers.py`

- [ ] **Step 1: Add scroll animation CSS**

Add to `styles/main.css`:

```css
/* Scroll-triggered animations */
.scroll-reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.scroll-reveal.revealed {
    opacity: 1;
    transform: translateY(0);
}

.scroll-reveal-left {
    opacity: 0;
    transform: translateX(-30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.scroll-reveal-left.revealed {
    opacity: 1;
    transform: translateX(0);
}

.scroll-reveal-right {
    opacity: 0;
    transform: translateX(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.scroll-reveal-right.revealed {
    opacity: 1;
    transform: translateX(0);
}

.scroll-reveal-scale {
    opacity: 0;
    transform: scale(0.9);
    transition: opacity 0.6s ease, transform 0.6s ease;
}

.scroll-reveal-scale.revealed {
    opacity: 1;
    transform: scale(1);
}
```

- [ ] **Step 2: Add Intersection Observer JavaScript**

Add JavaScript for scroll detection to `utils/helpers.py`:

```python
def inject_scroll_observer() -> None:
    """Inject JavaScript for scroll-triggered animations."""
    st.markdown("""
    <script>
    // Intersection Observer for scroll animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all elements with scroll-reveal classes
    document.addEventListener('DOMContentLoaded', () => {
        const elements = document.querySelectorAll(
            '.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .scroll-reveal-scale'
        );
        elements.forEach(el => observer.observe(el));
    });
    </script>
    """, unsafe_allow_html=True)
```

- [ ] **Step 3: Apply scroll animations to components**

Add scroll-reveal classes to component sections:

```python
# In components/about.py
def render_about():
    # ...
    st.markdown(f"""
    <div class="glass-card scroll-reveal">
        <!-- card content -->
    </div>
    """, unsafe_allow_html=True)
```

- [ ] **Step 4: Call scroll observer in app.py**

Add to `app.py` after CSS injection:

```python
from utils.helpers import inject_theme_and_css, inject_scroll_observer

inject_theme_and_css()
inject_scroll_observer()
```

- [ ] **Step 5: Verify scroll animations**

Scroll through the page and verify:
- Elements animate in when scrolled into view
- Animation triggers only once
- No performance issues
- Works on mobile

- [ ] **Step 6: Commit scroll animations**

```bash
git add styles/main.css utils/helpers.py app.py components/*.py
git commit -m "feat: add scroll-triggered animations with Intersection Observer"
```

---

### Task C3: Micro-interactions

**Files:**
- Modify: `styles/main.css`

- [ ] **Step 1: Add link animations**

```css
/* Animated Links */
.animated-link {
    position: relative;
    color: var(--accent-color);
    text-decoration: none;
    transition: color var(--transition-fast);
}

.animated-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-color), var(--accent-secondary));
    transition: width var(--transition-base);
    border-radius: 1px;
}

.animated-link:hover {
    color: var(--accent-secondary);
}

.animated-link:hover::after {
    width: 100%;
}
```

- [ ] **Step 2: Add icon animations**

```css
/* Icon Hover Effects */
.icon-rotate {
    transition: transform var(--transition-base);
}

.icon-rotate:hover {
    transform: rotate(360deg);
}

.icon-bounce {
    transition: transform var(--transition-fast);
}

.icon-bounce:hover {
    animation: bounce 0.5s ease;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-5px); }
}

.icon-pulse {
    transition: transform var(--transition-fast);
}

.icon-pulse:hover {
    animation: pulse 0.5s ease;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
```

- [ ] **Step 3: Add form field animations**

```css
/* Form Field Focus Effects */
.stTextInput input,
.stTextArea textarea,
.stSelectbox div {
    transition: all var(--transition-base) !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: var(--accent-color) !important;
    box-shadow: 0 0 0 3px rgba(79, 124, 255, 0.15) !important;
    transform: translateY(-1px);
}
```

- [ ] **Step 4: Add tag animations**

```css
/* Tech Tag Hover */
.tech-tag {
    transition: all var(--transition-fast) !important;
    cursor: default;
}

.tech-tag:hover {
    background: rgba(79, 124, 255, 0.2) !important;
    transform: translateY(-2px);
    box-shadow: var(--shadow-sm);
}
```

- [ ] **Step 5: Verify micro-interactions**

Test all interactive elements:
- Links have underline animation on hover
- Icons have rotation/bounce effects
- Form fields have focus glow
- Tags have subtle lift on hover

- [ ] **Step 6: Commit micro-interactions**

```bash
git add styles/main.css
git commit -m "feat: add micro-interactions for links, icons, and form fields"
```

---

### Task C4: Loading States

**Files:**
- Modify: `styles/main.css`
- Modify: `components/projects.py`
- Modify: `components/playground.py`

- [ ] **Step 1: Add skeleton loader CSS**

```css
/* Skeleton Loaders */
@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

.skeleton {
    background: linear-gradient(
        90deg,
        var(--card-bg) 25%,
        rgba(79, 124, 255, 0.1) 50%,
        var(--card-bg) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: var(--radius-md);
}

.skeleton-text {
    height: 16px;
    margin-bottom: 8px;
    width: 100%;
}

.skeleton-text.short {
    width: 60%;
}

.skeleton-title {
    height: 24px;
    margin-bottom: 12px;
    width: 80%;
}

.skeleton-card {
    height: 200px;
    width: 100%;
}

.skeleton-avatar {
    width: 48px;
    height: 48px;
    border-radius: var(--radius-full);
}
```

- [ ] **Step 2: Add loading skeleton to projects.py**

Add skeleton loader while GitHub repos are loading:

```python
elif view_mode == "Live GitHub Activity":
    # Show skeleton while loading
    st.markdown("""
    <div class="glass-card">
        <div class="skeleton skeleton-title"></div>
        <div class="skeleton skeleton-text"></div>
        <div class="skeleton skeleton-text short"></div>
        <div style="height: 20px;"></div>
        <div class="skeleton skeleton-card"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # ... rest of the code
```

- [ ] **Step 3: Add loading spinner to playground.py**

Enhance the existing spinners with custom styling:

```css
/* Custom Spinner */
.stSpinner > div {
    border-color: var(--accent-color) !important;
    border-top-color: transparent !important;
}
```

- [ ] **Step 4: Verify loading states**

Test:
- Skeleton appears while content loads
- Shimmer animation is smooth
- Spinner matches theme
- No layout shifts when content appears

- [ ] **Step 5: Commit loading states**

```bash
git add styles/main.css components/projects.py components/playground.py
git commit -m "feat: add skeleton loaders and enhanced loading states"
```

---

## Track D: Mobile & Responsiveness

### Task D1: Sidebar Responsiveness

**Files:**
- Modify: `styles/main.css:354-373`
- Modify: `app.py`

- [ ] **Step 1: Add mobile sidebar styles**

Update the responsive styles in `styles/main.css`:

```css
/* Mobile Sidebar */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 100% !important;
        min-width: 100% !important;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        z-index: 999 !important;
        transform: translateX(-100%);
        transition: transform var(--transition-base);
    }

    [data-testid="stSidebar"][aria-expanded="true"] {
        transform: translateX(0);
    }

    [data-testid="stSidebar"] > div {
        padding: var(--space-md) !important;
    }

    /* Sidebar overlay */
    [data-testid="stSidebar"]::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: -1;
        opacity: 0;
        transition: opacity var(--transition-base);
        pointer-events: none;
    }

    [data-testid="stSidebar"][aria-expanded="true"]::after {
        opacity: 1;
        pointer-events: auto;
    }

    /* Mobile menu button */
    .mobile-menu-btn {
        display: block !important;
        position: fixed;
        top: var(--space-md);
        left: var(--space-md);
        z-index: 1000;
        background: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: var(--radius-md);
        padding: var(--space-sm);
        cursor: pointer;
        box-shadow: var(--shadow-md);
    }
}

@media (min-width: 769px) {
    .mobile-menu-btn {
        display: none !important;
    }
}
```

- [ ] **Step 2: Add touch-friendly navigation**

```css
/* Touch-friendly targets */
@media (max-width: 768px) {
    .nav-link,
    .stButton > button,
    .custom-btn,
    .custom-btn-outline {
        min-height: 44px !important;
        min-width: 44px !important;
        padding: var(--space-sm) var(--space-md) !important;
    }

    /* Larger tap targets for sidebar */
    [data-testid="stSidebar"] .stButton > button {
        width: 100% !important;
        text-align: left !important;
        justify-content: flex-start !important;
    }
}
```

- [ ] **Step 3: Test mobile sidebar**

Test on mobile viewport:
- Sidebar collapses properly
- Touch targets are large enough
- Overlay closes sidebar
- Navigation works correctly

- [ ] **Step 4: Commit sidebar responsiveness**

```bash
git add styles/main.css
git commit -m "feat: improve mobile sidebar with touch-friendly targets"
```

---

### Task D2: Component Responsive Layouts

**Files:**
- Modify: `styles/main.css`
- Modify: `components/hero.py`
- Modify: `components/projects.py`
- Modify: `components/skills.py`
- Modify: `components/tech_stack.py`

- [ ] **Step 1: Add responsive grid system**

```css
/* Responsive Grid Utilities */
.grid-2 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--space-lg);
}

.grid-3 {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: var(--space-lg);
}

.grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: var(--space-lg);
}

@media (max-width: 1024px) {
    .grid-4 {
        grid-template-columns: repeat(3, 1fr);
    }
}

@media (max-width: 768px) {
    .grid-2,
    .grid-3,
    .grid-4 {
        grid-template-columns: repeat(2, 1fr);
        gap: var(--space-md);
    }
}

@media (max-width: 480px) {
    .grid-2,
    .grid-3,
    .grid-4 {
        grid-template-columns: 1fr;
    }
}
```

- [ ] **Step 2: Fix hero layout for mobile**

Update `components/hero.py` responsive styles:

```python
# Add responsive CSS
st.markdown("""
<style>
@media (max-width: 768px) {
    .hero-title {
        font-size: 2rem !important;
    }
    .hero-sub {
        font-size: 1.1rem !important;
    }
    .hero-desc {
        font-size: 0.95rem !important;
    }
    .hero-svg-wrap {
        max-width: 280px !important;
        margin: 0 auto;
    }
}
</style>
""", unsafe_allow_html=True)
```

- [ ] **Step 3: Fix project grid for mobile**

Update `components/projects.py` to use responsive grid:

```python
# Replace st.columns with responsive CSS
for i in range(0, len(filtered_projects), 2):
    st.markdown('<div class="grid-2">', unsafe_allow_html=True)
    for j in range(2):
        if i + j < len(filtered_projects):
            proj = filtered_projects[i + j]
            # ... render project card
    st.markdown('</div>', unsafe_allow_html=True)
```

- [ ] **Step 4: Fix tech stack grid for mobile**

Update `components/tech_stack.py`:

```python
# Use responsive grid instead of st.columns
st.markdown(f'<div class="grid-{min(len(group["items"]), 5)}">', unsafe_allow_html=True)
for item in group["items"]:
    # ... render tech icon
st.markdown('</div>', unsafe_allow_html=True)
```

- [ ] **Step 5: Test responsive layouts**

Test all pages at:
- 1920px (desktop)
- 1024px (tablet landscape)
- 768px (tablet portrait)
- 480px (mobile)
- 375px (small mobile)

- [ ] **Step 6: Commit responsive layouts**

```bash
git add styles/main.css components/hero.py components/projects.py components/skills.py components/tech_stack.py
git commit -m "feat: improve responsive layouts for all components"
```

---

### Task D3: Mobile Typography & Spacing

**Files:**
- Modify: `styles/main.css`

- [ ] **Step 1: Add mobile typography scale**

```css
/* Mobile Typography */
@media (max-width: 768px) {
    :root {
        --font-size-3xl: 1.75rem;
        --font-size-4xl: 2rem;
        --font-size-5xl: 2.5rem;
    }

    .section-header {
        font-size: var(--font-size-2xl) !important;
        margin-bottom: var(--space-xs) !important;
    }

    .section-subtitle {
        font-size: var(--font-size-md) !important;
        margin-bottom: var(--space-lg) !important;
    }

    h1 { font-size: var(--font-size-3xl) !important; }
    h2 { font-size: var(--font-size-2xl) !important; }
    h3 { font-size: var(--font-size-xl) !important; }
    h4 { font-size: var(--font-size-lg) !important; }
}

@media (max-width: 480px) {
    :root {
        --font-size-3xl: 1.5rem;
        --font-size-4xl: 1.75rem;
    }

    .section-header {
        font-size: var(--font-size-xl) !important;
    }
}
```

- [ ] **Step 2: Add mobile spacing adjustments**

```css
/* Mobile Spacing */
@media (max-width: 768px) {
    :root {
        --space-lg: 16px;
        --space-xl: 24px;
        --space-2xl: 32px;
        --space-3xl: 48px;
    }

    div.block-container {
        padding: var(--space-md) !important;
        padding-top: var(--space-lg) !important;
    }

    .glass-card {
        padding: var(--space-md) !important;
        margin-bottom: var(--space-md) !important;
    }

    .stat-card {
        padding: var(--space-sm) !important;
    }
}
```

- [ ] **Step 3: Verify mobile typography**

Check on mobile:
- Text is readable (minimum 16px body)
- Headings have clear hierarchy
- Spacing is comfortable
- No text overflow

- [ ] **Step 4: Commit mobile typography**

```bash
git add styles/main.css
git commit -m "feat: optimize typography and spacing for mobile devices"
```

---

## Phase 5: Final Polish

### Task F1: Cross-Browser Testing

**Files:**
- None (testing only)

- [ ] **Step 1: Test in Chrome**

Verify all features work in Chrome:
- Animations smooth
- Glassmorphism renders
- Layout correct
- No console errors

- [ ] **Step 2: Test in Firefox**

Verify all features work in Firefox:
- CSS variables work
- Backdrop filter works
- Animations smooth
- Layout correct

- [ ] **Step 3: Test in Safari**

Verify all features work in Safari:
- Webkit prefixes work
- Glassmorphism renders
- Animations smooth
- Layout correct

- [ ] **Step 4: Test on mobile browsers**

Test on:
- Chrome Mobile
- Safari Mobile
- Samsung Internet

- [ ] **Step 5: Document browser compatibility**

Create note of any browser-specific issues found.

---

### Task F2: Performance Audit

**Files:**
- None (testing only)

- [ ] **Step 1: Run Lighthouse audit**

Run Chrome Lighthouse on the deployed app:
```bash
# If deployed to Streamlit Cloud
# Open Chrome DevTools > Lighthouse > Generate Report
```

Target scores:
- Performance: > 90
- Accessibility: > 90
- Best Practices: > 90
- SEO: > 90

- [ ] **Step 2: Check for performance issues**

Common issues to check:
- Large CSS file size
- Unoptimized images
- Render-blocking resources
- Excessive DOM size

- [ ] **Step 3: Optimize if needed**

Based on audit results:
- Minimize CSS if too large
- Optimize image delivery
- Reduce DOM complexity

---

### Task F3: Accessibility Audit

**Files:**
- Modify: `styles/main.css`
- Modify: `components/*.py`

- [ ] **Step 1: Add ARIA labels**

Add ARIA labels to interactive elements:

```python
# In components
st.markdown("""
<a href="..." aria-label="Visit GitHub profile" ...>
    ...
</a>
""", unsafe_allow_html=True)
```

- [ ] **Step 2: Improve color contrast**

Ensure all text meets WCAG AA contrast ratios:
- Normal text: 4.5:1
- Large text: 3:1

- [ ] **Step 3: Add keyboard navigation**

Ensure all interactive elements are keyboard accessible:
- Tab order is logical
- Focus indicators are visible
- Skip navigation link exists

- [ ] **Step 4: Test with screen reader**

Test with VoiceOver (Mac) or NVDA (Windows):
- All content is readable
- Navigation is logical
- Images have alt text

---

## Execution Order

### Parallel Execution Groups

**Group 1 (Start immediately):**
- Task A1: Design Tokens
- Task B1: Error Handling
- Task C1: Page Transitions

**Group 2 (After Group 1):**
- Task A2: Glassmorphism
- Task B2: Type Hints
- Task C2: Scroll Animations
- Task D1: Sidebar Responsiveness

**Group 3 (After Group 2):**
- Task A3: Typography
- Task B3: State Management
- Task C3: Micro-interactions
- Task D2: Component Layouts

**Group 4 (After Group 3):**
- Task A4: Buttons
- Task C4: Loading States
- Task D3: Mobile Typography

**Group 5 (Final):**
- Task F1: Cross-Browser Testing
- Task F2: Performance Audit
- Task F3: Accessibility Audit

---

## Success Criteria

1. **Visual**: Premium glassmorphism design with smooth animations
2. **Mobile**: Perfect experience on all devices (375px to 1920px)
3. **Performance**: Fast load times, smooth 60fps animations
4. **Code**: Clean, typed, well-documented codebase
5. **Accessibility**: WCAG 2.1 AA compliant
6. **Browser**: Works in Chrome, Firefox, Safari, Edge
