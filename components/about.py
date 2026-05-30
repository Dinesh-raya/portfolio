# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary

@error_boundary
def render_about():
    about_data = PORTFOLIO_DATA["about"]
    personal = PORTFOLIO_DATA["personal"]
    
    st.markdown('<div class="section-header">About Me</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>My engineering background, journey, and developer setup.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.1, 0.9], gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 25px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🎯</span> Professional Summary
            </h4>
            <p style="color: var(--text-color); font-size: 1.05rem; line-height: 1.6; margin: 0;">
                {about_data['summary']}
            </p>
        </div>
        
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>🚀</span> My Coding Journey
            </h4>
            <p style="color: var(--text-muted); font-size: 1rem; line-height: 1.6; margin: 0;">
                {about_data['journey']}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        # Info Card
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 25px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>ℹ️</span> Details & Credentials
            </h4>
            <div style="display: grid; gap: 15px;">
                <div>
                    <strong style="color: var(--text-color);">📍 Location:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">{personal['location']}</div>
                </div>
                <div>
                    <strong style="color: var(--text-color);">📧 Email:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">
                        <a href="mailto:{personal['email']}" style="color: var(--accent-color); text-decoration: none;">{personal['email']}</a>
                    </div>
                </div>
                <div>
                    <strong style="color: var(--text-color);">🗣️ Languages:</strong>
                    <div style="color: var(--text-muted); margin-top: 2px;">{", ".join(about_data['languages'])}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Education Card
        edu_html = ""
        for edu in about_data["education"]:
            edu_html += f"""
            <div style="margin-bottom: 10px;">
                <div style="font-weight: 600; color: var(--text-color);">{edu['degree']}</div>
                <div style="font-size: 0.9rem; color: var(--accent-color);">{edu['institution']}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">{edu['year']}</div>
            </div>
            """
            
        st.markdown(f"""
        <div class="glass-card" style="margin-bottom: 25px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>🎓</span> Education
            </h4>
            {edu_html}
        </div>
        """, unsafe_allow_html=True)
        
        # Workspace Preferences
        ws = about_data["workspace_info"]
        st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 16px; display: flex; align-items: center; gap: 8px;">
                <span>💻</span> Workspace Setup
            </h4>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-size: 0.95rem;">
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">OS</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['os']}</div>
                </div>
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Editor</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['editor']}</div>
                </div>
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Terminal</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['terminal']}</div>
                </div>
                <div>
                    <div style="color: var(--text-muted); font-size: 0.85rem;">Vibe</div>
                    <div style="font-weight: 600; color: var(--text-color);">{ws['vibe']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
