# Portfolio Code Audit Report

**Date:** 2026-05-30
**Auditor:** Fork Agent
**Scope:** Overall code quality audit of Streamlit portfolio

---

## CRITICAL Issues (Will cause runtime/visual errors)

### 1. Duplicate CSS `@keyframes shimmer` Definition
- **File:** `styles/main.css`
- **Lines:** 749 and 905
- **Issue:** Two identical `@keyframes shimmer` definitions. Browsers handle this unpredictably — the second definition silently overrides the first. While both are identical, this indicates copy-paste without cleanup.
- **Fix:** Remove the duplicate at line 905.

### 2. Hardcoded Dark Gradients in Project Cards
- **File:** `components/projects.py`
- **Lines:** 76-80
- **Issue:** Project illustration backgrounds use hardcoded dark colors (`#1e293b`, `#0f172a`, `#111e38`, `#10162f`, `#0b2530`, `#081a24`). These will look terrible in light mode — dark rectangles on a light background.
- **Fix:** Use CSS variables like `var(--card-bg)` or `var(--surface-subtle)` with accent color overlays.

---

## IMPORTANT Issues (Causes visual bugs or poor UX)

### 3. Hardcoded Green Colors Not Using CSS Variables
- **File:** `components/contact.py` line 83 — `color: #00d464`
- **File:** `components/playground.py` line 461 — `color: "#00d464"`, `"#f59e0b"`, `"#ef4444"`
- **File:** `styles/main.css` line 158 — `background: #22c55e`
- **Issue:** These colors don't respond to theme changes. While green works in both modes, consistency requires using CSS variables.
- **Fix:** Define `--color-success`, `--color-warning`, `--color-error` in theme vars.

### 4. Inconsistent HTML Rendering Approach
- **Files:** All component files
- **Issue:** Mix of `st.markdown(html, unsafe_allow_html=True)` and `render_html()` (which uses `st.html()`). The `render_html()` function uses `st.html()` which is more reliable for complex HTML. Using `st.markdown` with `unsafe_allow_html` can cause certain HTML tags to be escaped or rendered as text.
- **Fix:** Standardize all HTML rendering to use `render_html()` from helpers.py.

### 5. Unused Import in playground.py
- **File:** `components/playground.py` line 3
- **Issue:** `import textwrap` is imported but never used.
- **Fix:** Remove the import.

### 6. CSS `@import` Blocks Rendering
- **File:** `styles/main.css` line 4
- **Issue:** `@import url('https://fonts.googleapis.com/css2?family=Outfit...')` is a render-blocking resource. In Streamlit, this CSS is injected via `<style>` tag, so the browser must fetch the font before rendering.
- **Fix:** Load the font via `<link>` tag in app.py head, or use `st.html()` to inject it early.

---

## MINOR Issues (Code quality/style)

### 7. Hardcoded Colors in Inline Styles
- **Files:** Multiple components
- **Issue:** Several inline styles use hardcoded color values instead of CSS variables (e.g., `rgba(79, 124, 255, 0.25)` instead of `var(--accent-glow)`).
- **Impact:** Low — these colors are accent-related and work in both themes, but violate the design token system.

### 8. No `alt` Text on Some Images
- **File:** `components/tech_stack.py` line 34
- **Issue:** While `alt` text is provided, `onerror="this.style.display='none'"` hides broken images silently with no fallback.
- **Impact:** Low — accessibility concern.

---

## Test Coverage Assessment

- **17/17 tests passing**
- Tests cover: component imports, data structure validation, utility functions, content loading, smoke tests
- **Missing tests:** Form submission validation edge cases, CSS variable injection, theme toggle behavior

---

## Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 2 |
| IMPORTANT | 4 |
| MINOR | 2 |

**Overall Rating: 7.5/10**

The portfolio has solid architecture and good separation of concerns. The main issues are:
1. Light mode visual bugs from hardcoded dark colors
2. Inconsistent HTML rendering approach
3. Duplicate CSS definitions

Fixing the CRITICAL and IMPORTANT issues would bring this to **8.5-9/10**.
