# -*- coding: utf-8 -*-
import os
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, render_html
from utils.icons import icon




def _render_typewriter() -> None:
    roles = '["AI Engineer","Problem Solver","Python Developer","ML Enthusiast","Automation Builder","Open Source Contributor"]'
    html = (
        '<div style="font-size:1.3rem;text-transform:uppercase;color:#4F7CFF;font-weight:700;letter-spacing:0.06em;font-family:Outfit,sans-serif;overflow:hidden;">'
        '<span id="tw"></span><span id="tc" style="animation:blink .8s step-end infinite;">|</span>'
        '<style>@keyframes blink{50%{opacity:0}}</style>'
        '<script>'
        '(function(){'
        'var r=' + roles + ';var i=0,c=0,d=false,e=document.getElementById("tw");'
        '(function t(){'
        'if(!e)return;var w=r[i];'
        'if(!d){e.textContent=w.substring(0,c+1);c++;if(c===w.length){d=true;setTimeout(t,2000);return}}'
        'else{e.textContent=w.substring(0,c-1);c--;if(c===0){d=false;i=(i+1)%r.length;setTimeout(t,500);return}}'
        'setTimeout(t,d?40:80);'
        '})();'
        '})();'
        '</script></div>'
    )
    from urllib.parse import quote
    data_uri = "data:text/html;charset=utf-8," + quote(html)
    st.iframe(src=data_uri, height=32)


@error_boundary
def render_hero() -> None:
    """Sleek and professional introductory landing page (Home)."""
    personal = PORTFOLIO_DATA["personal"]
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
                    f'<a href="{personal["linkedin"]}" target="_blank" '
                    f'class="custom-btn-outline" style="display:flex; height:44px; align-items:center; '
                    f'justify-content:center; width:100%; font-size:0.95rem;">View LinkedIn</a>'
                )

        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

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
            <div>{icon('mail', 16)} <strong>Email:</strong> <a href="mailto:{personal['email']}">{personal['email']}</a></div>
        </div>
        """)

