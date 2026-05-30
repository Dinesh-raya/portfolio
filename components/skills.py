# -*- coding: utf-8 -*-
import streamlit as st
import plotly.graph_objects as go
from data.portfolio_data import PORTFOLIO_DATA

def render_skills():
    skills_data = PORTFOLIO_DATA["skills"]
    radar_data = skills_data["radar"]
    theme = st.session_state.get("theme", "dark")
    
    st.markdown('<div class="section-header">Skills & Competency</div>', unsafe_allow_html=True)
    st.markdown("<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>Interactive analysis of engineering competencies and skill domains.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.25rem; margin-bottom: 15px;">
                🧠 Competency Radar Chart
            </h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.5; margin-bottom: 20px;">
                An interactive map of my technical strengths across main developer and artificial intelligence domains.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Plotly Radar Chart
        categories = radar_data["metrics"]
        values = radar_data["values"]
        
        # Plotly polar graph
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(79, 124, 255, 0.25)',
            line=dict(color='#4F7CFF', width=2),
            marker=dict(color='#00D4FF', size=6),
            name='Proficiency'
        ))
        
        # Styling based on theme
        grid_color = "rgba(160, 174, 192, 0.2)" if theme == "dark" else "rgba(107, 114, 128, 0.2)"
        text_color = "#F5F7FA" if theme == "dark" else "#111827"
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    showticklabels=False,
                    gridcolor=grid_color,
                    linecolor=grid_color
                ),
                angularaxis=dict(
                    gridcolor=grid_color,
                    linecolor=grid_color,
                    tickfont=dict(size=10, color=text_color)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=40, t=20, b=20),
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
    with col2:
        st.markdown("<h4 style='color: var(--text-color); font-weight: 700; font-size: 1.3rem; margin-bottom: 20px;'>Skill Matrix</h4>", unsafe_allow_html=True)
        
        for category in skills_data["categories"]:
            pills = "".join([f'<span class="tech-tag" style="font-size: 0.85rem; padding: 6px 12px; margin-bottom: 8px;">{item}</span>' for item in category["items"]])
            st.markdown(f"""
            <div class="glass-card" style="margin-bottom: 20px;">
                <h5 style="color: var(--accent-color); font-weight: 700; font-size: 1.15rem; margin-bottom: 12px; display: flex; align-items: center; gap: 6px;">
                    <span>📂</span> {category['title']}
                </h5>
                <div style="display: flex; flex-wrap: wrap;">
                    {pills}
                </div>
            </div>
            """, unsafe_allow_html=True)
