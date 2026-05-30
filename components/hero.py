# -*- coding: utf-8 -*-
import os
import streamlit as st
import plotly.graph_objects as go
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
    categories = skills["radar"]["metrics"]
    values = skills["radar"]["values"]
    colors = plotly_polar_theme(theme)
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor="rgba(79, 124, 255, 0.18)",
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


@error_boundary
def render_hero() -> None:
    """Single-page executive dashboard (Home)."""
    personal = PORTFOLIO_DATA["personal"]
    stats = PORTFOLIO_DATA["stats"]
    about = PORTFOLIO_DATA["about"]
    projects = PORTFOLIO_DATA["projects"]
    skills = PORTFOLIO_DATA["skills"]
    tech_stack = PORTFOLIO_DATA["tech_stack"]
    experience = PORTFOLIO_DATA.get("experience", [])
    articles = load_articles()
    theme = st.session_state.get("theme", "dark")
    first_name = personal["name"].split()[0]
    photo_path = personal.get("photo", "") or ""
    has_photo = photo_path and os.path.isfile(photo_path)
    resume_path = "assets/dinesh_raya.pdf"
    has_resume = os.path.isfile(resume_path)

    render_html(
        '<div class="dash-status-pill"><span class="status-dot"></span> Available for collaboration</div>'
    )

    header_left, header_right = st.columns([2, 1])
    with header_left:
        render_html(
            '<p class="header-subtitle" style="margin:0;">&gt; Building solutions with code and creativity.</p>'
        )
    with header_right:
        btn_cols = st.columns(2)
        with btn_cols[0]:
            if has_resume:
                with open(resume_path, "rb") as f:
                    resume_data = f.read()
                st.download_button(
                    label="Resume",
                    data=resume_data,
                    file_name=personal["resume_name"],
                    mime="application/pdf",
                    key="dash_resume_download",
                    use_container_width=True,
                )
            else:
                render_html(
                    f'<a href="mailto:{personal["email"]}?subject=Resume%20Request" '
                    f'class="custom-btn-outline" style="display:flex;height:38px;align-items:center;'
                    f'justify-content:center;width:100%;font-size:0.82rem;">Request Resume</a>'
                )
                if os.environ.get("STREAMLIT_RUNTIME_ENVIRONMENT") != "cloud":
                    st.caption("Add assets/dinesh_raya.pdf to enable PDF download.")
        with btn_cols[1]:
            render_html(
                f'<a href="mailto:{personal["email"]}" class="custom-btn-outline" '
                f'style="display:flex;height:38px;align-items:center;justify-content:center;width:100%;font-size:0.82rem;">Let\'s Chat</a>'
            )

    row1_col1, row1_col2, row1_col3 = st.columns([1.1, 0.9, 1.0], gap="medium")

    with row1_col1:
        with st.container(border=True):
            if has_photo:
                pic_col, text_col = st.columns([1, 2.2])
                with pic_col:
                    st.image(photo_path, width=120)
                with text_col:
                    render_html(_profile_header_html(personal))
            else:
                render_html(f"""
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
                    <div class="sidebar-monogram" style="width:50px;height:50px;font-size:1.2rem;margin:0;">DR</div>
                    {_profile_header_html(personal)}
                </div>
                """)
            render_html(f"""
            <h1 style="font-size:2rem;font-weight:800;line-height:1.1;margin:0 0 10px;">
                Hi, I'm <span class="gradient-text">{first_name}</span>
            </h1>
            <p style="font-size:0.92rem;color:var(--text-muted);line-height:1.5;margin:0;">
                {personal['short_description']}
            </p>
            <div class="mini-stat-grid">
                <div class="mini-stat"><div class="mini-stat-value">{stats[0]['value']}</div><div class="mini-stat-label">{stats[0]['label']}</div></div>
                <div class="mini-stat"><div class="mini-stat-value">{stats[1]['value']}</div><div class="mini-stat-label">{stats[1]['label']}</div></div>
                <div class="mini-stat"><div class="mini-stat-value">{stats[2]['value']}</div><div class="mini-stat-label">{stats[2]['label']}</div></div>
                <div class="mini-stat"><div class="mini-stat-value">{stats[3]['value']}</div><div class="mini-stat-label">{stats[3]['label']}</div></div>
            </div>
            """)
            b1, b2 = st.columns(2)
            with b1:
                render_html(
                    f'<a href="{personal["github"]}" target="_blank" class="custom-btn" '
                    f'style="display:flex;height:38px;align-items:center;justify-content:center;width:100%;font-size:0.82rem;">View My Work</a>'
                )
            with b2:
                render_html(
                    f'<a href="{personal["github"]}" target="_blank" class="custom-btn-outline" '
                    f'style="display:flex;height:38px;align-items:center;justify-content:center;width:100%;font-size:0.82rem;">Browse GitHub</a>'
                )

    with row1_col2:
        with st.container(border=True):
            render_html(_dash_title("📊", "Skills Snapshot"))
            st.plotly_chart(_radar_chart(skills, theme), use_container_width=True, config={"displayModeBar": False})
            render_html(_skill_bars_html(skills["radar"]["metrics"], skills["radar"]["values"]))

    with row1_col3:
        with st.container(border=True):
            render_html(_dash_title("⚡", "Featured Projects") + _projects_html(projects, 3))
            gh_user = personal.get("github_username", "Dinesh-raya")
            with st.spinner("Loading GitHub highlights…"):
                gh_repos = github_fetch_repos(gh_user)
            render_html(_github_repos_html(gh_repos, 3, personal["github"]))
            render_html(
                f'<a href="{personal["github"]}" target="_blank" class="custom-btn-outline" '
                f'style="display:flex;height:38px;align-items:center;justify-content:center;width:100%;font-size:0.82rem;">See All Projects</a>'
            )

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    row2_col1, row2_col2, row2_col3 = st.columns([1.0, 1.0, 1.0], gap="medium")

    with row2_col1:
        with st.container(border=True):
            summary = about["summary"][:200] + ("..." if len(about["summary"]) > 200 else "")
            render_html(f"""
            {_dash_title("👤", "About Me")}
            <p style="font-size:0.85rem;color:var(--text-muted);line-height:1.45;margin:0 0 8px;">{summary}</p>
            <div class="about-meta">
                <div>Location: <span style="color:var(--text-muted);">{personal['location']}</span></div>
                <div>Education: <span style="color:var(--text-muted);">{about['education'][0]['degree']}</span></div>
                <div>Email: <span style="color:var(--text-muted);">{personal['email']}</span></div>
            </div>
            """)

    with row2_col2:
        with st.container(border=True):
            stack_items = tech_stack[0]["items"][:4] + tech_stack[1]["items"][:4]
            render_html(_dash_title("🧩", "Tech Stack") + _tech_grid_html(stack_items))

    with row2_col3:
        with st.container(border=True):
            drives_html = ""
            for drive in personal.get("drives", []):
                drives_html += f'<div class="drives-card"><div class="drives-icon">{drive["icon"]}</div><div class="drives-title">{drive["title"]}</div></div>'
            render_html(
                _dash_title("🔥", "What Drives Me")
                + f'<div class="drives-row">{drives_html}</div>'
            )

    st.markdown("<div class='spacer-sm'></div>", unsafe_allow_html=True)
    row3_col1, row3_col2, row3_col3 = st.columns([1.1, 0.9, 1.0], gap="medium")

    with row3_col1:
        with st.container(border=True):
            render_html(_dash_title("🕐", "Experience & Journey") + _timeline_html(experience))

    with row3_col2:
        with st.container(border=True):
            render_html(_dash_title("📝", "Latest Articles") + _articles_html(articles, 3, personal.get("linkedin", "#")))

    with row3_col3:
        with st.container(border=True):
            render_html(_dash_title("✉️", "Let's Connect"))
            with st.form("dash_contact_form", clear_on_submit=True):
                name_input = st.text_input("Name", placeholder="Your Name", label_visibility="collapsed")
                email_input = st.text_input("Email", placeholder="Your Email", label_visibility="collapsed")
                msg_input = st.text_area(
                    "Message", placeholder="Write your message...", height=72, label_visibility="collapsed"
                )
                submitted = st.form_submit_button("Send Message", use_container_width=True)
            if submitted:
                ok, msg = send_contact_form(
                    name_input,
                    email_input,
                    "Portfolio dashboard",
                    msg_input,
                    source="home_dashboard",
                )
                if ok:
                    st.success(msg)
                else:
                    st.warning(msg)
