# -*- coding: utf-8 -*-
import json
import os
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import (
    get_tech_icon_url,
    error_boundary,
    render_html,
    send_contact_form,
    github_fetch_repos,
    plotly_polar_theme,
    load_articles,
)


def _dash_title(icon: str, label: str) -> str:
    return f'<h4 class="dash-card-title"><span>{icon}</span> {label}</h4>'


def _skill_bars_html(metrics: list, values: list, limit: int = 3) -> str:
    pairs = sorted(zip(metrics, values), key=lambda x: x[1], reverse=True)[:limit]
    rows = []
    for name, pct in pairs:
        short = name.split()[0] if len(name) > 12 else name
        rows.append(f"""
        <div class="skill-progress-bar-wrapper">
            <div class="skill-progress-label-row">
                <span>{short}</span><span>{pct}%</span>
            </div>
            <div class="skill-progress-track">
                <div class="skill-progress-fill" style="width: {pct}%;"></div>
            </div>
        </div>""")
    return f'<div class="skills-progress-container">{"".join(rows)}</div>'


def _project_links_html(proj: dict) -> str:
    links = []
    gh = proj.get("github", "")
    demo = proj.get("demo", "")
    if gh and gh != "#":
        links.append(f'<a href="{gh}" target="_blank" class="project-link">GitHub</a>')
    if demo and demo not in ("#", ""):
        links.append(f'<a href="{demo}" target="_blank" class="project-link">Live</a>')
    if not links:
        return ""
    return f'<div class="project-mini-links">{"".join(links)}</div>'


def _projects_html(projects: list, limit: int = 3) -> str:
    cards = []
    for proj in projects[:limit]:
        desc = proj["description"][:85] + ("..." if len(proj["description"]) > 85 else "")
        cards.append(f"""
        <div class="project-mini-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-weight:700;font-size:0.9rem;color:var(--text-color);">{proj['title']}</span>
                <span style="font-size:0.72rem;text-transform:uppercase;color:var(--accent-color);font-weight:700;">{proj['category']}</span>
            </div>
            <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;line-height:1.35;">{desc}</div>
            {_project_links_html(proj)}
        </div>""")
    return "".join(cards)


def _github_repos_html(repos: list, limit: int = 3, github_url: str = "https://github.com/Dinesh-raya") -> str:
    if not repos:
        return f"""
        <p class="github-from-label">From GitHub</p>
        <div class="project-mini-card github-repo-card" style="text-align:center;padding:20px;">
            <div style="font-size:1.4rem;margin-bottom:6px;">📦</div>
            <div style="font-weight:700;font-size:0.9rem;color:var(--text-color);margin-bottom:6px;">Explore My Repositories</div>
            <div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:12px;">Open-source projects, automation tools, and AI experiments</div>
            <a href="{github_url}" target="_blank" class="project-link" style="display:inline-block;">Browse GitHub →</a>
        </div>"""
    cards = []
    for repo in repos[:limit]:
        desc = (repo.get("description") or "Open-source project")[:80]
        if len(desc) >= 80:
            desc += "..."
        lang = repo.get("language") or "Code"
        stars = repo.get("stargazers_count", 0)
        cards.append(f"""
        <div class="project-mini-card github-repo-card">
            <div style="display:flex;justify-content:space-between;align-items:center;">
                <span style="font-weight:700;font-size:0.9rem;color:var(--text-color);">{repo['name']}</span>
                <span style="font-size:0.72rem;color:var(--text-muted);">{lang} · {stars} stars</span>
            </div>
            <div style="font-size:0.78rem;color:var(--text-muted);margin-top:4px;line-height:1.35;">{desc}</div>
            <div class="project-mini-links">
                <a href="{repo['html_url']}" target="_blank" class="project-link">Repository</a>
            </div>
        </div>""")
    return (
        '<p class="github-from-label">From GitHub</p>'
        + "".join(cards)
    )


def _tech_grid_html(items: list) -> str:
    cells = []
    for item in items:
        icon_url = get_tech_icon_url(item["icon_svg"])
        cells.append(f"""
        <div class="tech-icon-cell">
            <img src="{icon_url}" alt="{item['name']}" />
            <span>{item['name']}</span>
        </div>""")
    return f'<div class="tech-icon-grid">{"".join(cells)}</div>'


def _timeline_html(experience: list) -> str:
    nodes = []
    for item in experience:
        title = item["title"][:22] + ("…" if len(item["title"]) > 22 else "")
        nodes.append(f"""
        <div class="timeline-h-node">
            <div class="timeline-h-dot"></div>
            <div class="timeline-h-year">{item['period']}</div>
            <div class="timeline-h-title">{title}</div>
        </div>""")
    return f'<div class="timeline-horizontal">{"".join(nodes)}</div>'


def _articles_html(articles: list, limit: int = 3, linkedin_url: str = "#") -> str:
    if not articles:
        return f"""
        <div class="article-mini-card" style="text-align:center;padding:20px;">
            <div style="font-size:1.4rem;margin-bottom:6px;">✍️</div>
            <div style="font-weight:700;font-size:0.9rem;color:var(--text-color);margin-bottom:6px;">Articles Coming Soon</div>
            <div style="font-size:0.78rem;color:var(--text-muted);margin-bottom:12px;">Deep dives on AI, Python, and engineering</div>
            <a href="{linkedin_url}" target="_blank" class="project-link" style="display:inline-block;">Follow on LinkedIn →</a>
        </div>"""
    cards = []
    for art in articles[:limit]:
        cards.append(f"""
        <div class="article-mini-card">
            <div style="font-weight:600;font-size:0.85rem;color:var(--text-color);line-height:1.3;">{art['title']}</div>
            <div style="display:flex;justify-content:space-between;font-size:0.72rem;color:var(--text-muted);margin-top:4px;">
                <span>{art['date']}</span><span>{art['read_time']}</span>
            </div>
        </div>""")
    return "".join(cards)


def _radar_chart(skills: dict, theme: str):
    import plotly.graph_objects as go
    categories = skills["radar"]["metrics"]
    values = skills["radar"]["values"]
    colors = plotly_polar_theme(theme)
    fill_opacity = "0.10" if theme == "light" else "0.18"
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba(79, 124, 255, {fill_opacity})",
            line=dict(color="#4F7CFF", width=2),
            marker=dict(color="#00D4FF", size=4),
            name="Proficiency",
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                showticklabels=False,
                gridcolor=colors["grid"],
                linecolor=colors["grid"],
            ),
            angularaxis=dict(
                gridcolor=colors["grid"],
                linecolor=colors["grid"],
                tickfont=dict(size=8, color=colors["text"]),
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=25, r=25, t=10, b=10),
        height=170,
    )
    return fig


def _profile_header_html(personal: dict) -> str:
    return f"""
    <div>
        <div style="font-size:0.8rem;text-transform:uppercase;color:var(--accent-color);font-weight:700;">{personal.get('role', 'AI Enthusiast')}</div>
        <div style="font-weight:700;font-size:1.15rem;color:var(--text-color);">{personal['name']}</div>
    </div>
    """


def _render_typewriter() -> None:
    roles = ["AI Engineer", "Problem Solver", "Python Developer", "ML Enthusiast", "Automation Builder", "Open Source Contributor"]
    html = f"""<div style="font-size:1.3rem;text-transform:uppercase;color:#4F7CFF;font-weight:700;letter-spacing:0.06em;font-family:Outfit,sans-serif;overflow:hidden;">
<span id="tw"></span><span id="tc" style="animation:blink .8s step-end infinite;">|</span>
<style>@keyframes blink{{50%{{opacity:0}}}}</style>
<script>
(function(){{
var r={json.dumps(roles)};var i=0,c=0,d=false,e=document.getElementById('tw');
(function t(){{
if(!e)return;var w=r[i];
if(!d){{e.textContent=w.substring(0,c+1);c++;if(c===w.length){{d=true;setTimeout(t,2000);return}}}}
else{{e.textContent=w.substring(0,c-1);c--;if(c===0){{d=false;i=(i+1)%r.length;setTimeout(t,500);return}}}}
setTimeout(t,d?40:80);
}})();
}})();
</script></div>"""
    st.iframe(srcDoc=html, height=32, scrolling=False)


@error_boundary
def render_hero() -> None:
    """Sleek and professional introductory landing page (Home)."""
    personal = PORTFOLIO_DATA["personal"]
    stats = PORTFOLIO_DATA["stats"]
    photo_path = personal.get("photo", "") or ""
    has_photo = photo_path and os.path.isfile(photo_path)
    resume_path = "assets/dinesh_raya.pdf"
    has_resume = os.path.isfile(resume_path)

    # 1. Available Status Badge
    render_html(
        '<div class="dash-status-pill"><span class="status-dot"></span> Available for new opportunities</div>'
    )

    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

    # 2. Main 2-Column Hero Layout
    col_content, col_photo = st.columns([1.3, 0.9], gap="large")

    with col_content:
        # Title and Description
        render_html(f"""
        <h1 style="font-size:3.5rem; font-weight:800; line-height:1.15; margin:10px 0 10px;">
            Hi, I'm <span class="gradient-text">{personal['name']}</span>
        </h1>
        <p style="font-size:1.15rem; color:var(--text-muted); line-height:1.65; margin-bottom:30px; max-width:620px;">
            {personal['short_description']}
        </p>
        """)
        _render_typewriter()

        # Call-To-Action buttons
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            render_html(
                f'<a href="mailto:{personal["email"]}?subject=Collaboration" class="custom-btn" '
                f'style="display:flex; height:44px; align-items:center; justify-content:center; width:100%; font-size:0.95rem;">Hire Me / Let\'s Chat</a>'
            )
        with btn_col2:
            if has_resume:
                with open(resume_path, "rb") as f:
                    resume_data = f.read()
                st.download_button(
                    label="Download Resume",
                    data=resume_data,
                    file_name=personal["resume_name"],
                    mime="application/pdf",
                    key="hero_resume_download",
                )
            else:
                render_html(
                    f'<a href="mailto:{personal["email"]}?subject=Resume%20Request" '
                    f'class="custom-btn-outline" style="display:flex; height:44px; align-items:center; '
                    f'justify-content:center; width:100%; font-size:0.95rem;">Request Resume</a>'
                )

        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

        # 3. Highlighted Statistics Banner
        stats_html = ""
        for stat in stats:
            stats_html += f"""
            <div class="hero-stat-card">
                <div class="hero-stat-value">{stat['value']}</div>
                <div class="hero-stat-label">{stat['label']}</div>
            </div>"""
        
        render_html(f"""
        <div class="hero-stats-banner">
            {stats_html}
        </div>
        """)

    with col_photo:
        # Photo rendering
        if has_photo:
            import base64
            try:
                with open(photo_path, "rb") as img_file:
                    img_b64 = base64.b64encode(img_file.read()).decode("utf-8")
                render_html(f"""
                <div class="hero-photo-container">
                    <img src="data:image/jpeg;base64,{img_b64}" class="hero-profile-pic" />
                </div>
                """)
            except Exception:
                has_photo = False
        
        if not has_photo:
            render_html("""
            <div class="hero-photo-container">
                <div class="hero-profile-monogram">DR</div>
            </div>
            """)

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Sleek mini details card
        render_html(f"""
        <div class="hero-details-card">
            <div style="margin-bottom:8px;">📍 <strong>Location:</strong> {personal['location']}</div>
            <div>📧 <strong>Email:</strong> <a href="mailto:{personal['email']}">{personal['email']}</a></div>
        </div>
        """)

