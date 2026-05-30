# -*- coding: utf-8 -*-
import streamlit as st
import os
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary

@error_boundary
def render_hero() -> None:
    """Render the Hero/Home section with animated stats and CTAs."""
    personal = PORTFOLIO_DATA["personal"]
    stats    = PORTFOLIO_DATA["stats"]
    theme    = st.session_state.get("theme", "dark")

    # ── Animated-counter CSS (injected once per load) ─────────────────────────
    st.markdown("""
    <style>
    @keyframes countUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0);    }
    }
    .stat-card { animation: countUp 0.6s ease forwards; }
    .stat-card:nth-child(2) { animation-delay: 0.1s; }
    .stat-card:nth-child(3) { animation-delay: 0.2s; }
    .stat-card:nth-child(4) { animation-delay: 0.3s; }

    @keyframes floatSvg {
        0%, 100% { transform: translateY(0px);   }
        50%      { transform: translateY(-10px);  }
    }
    .hero-svg-wrap { animation: floatSvg 4s ease-in-out infinite; }

    /* Gradient animated text shimmer */
    @keyframes shimmer {
        0%   { background-position: -200% center; }
        100% { background-position:  200% center; }
    }
    .gradient-text {
        background: linear-gradient(90deg, #4F7CFF, #00D4FF, #4F7CFF);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shimmer 3s linear infinite;
    }

    /* Responsive hero heading */
    @media (max-width: 768px) {
        .hero-title  { font-size: 2.2rem !important; }
        .hero-sub    { font-size: 1.1rem !important; }
        .hero-desc   { font-size: 0.95rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8], gap="large")

    # ── Left: Text + CTA ─────────────────────────────────────────────────────
    with col1:
        st.markdown(f"""
        <div style='margin-top: 20px;'>
            <div style='
                display: inline-block;
                background: rgba(79,124,255,0.1);
                border: 1px solid rgba(79,124,255,0.25);
                border-radius: 30px; padding: 5px 14px;
                font-size: 0.82rem; font-weight: 600;
                color: var(--accent-color); margin-bottom: 18px;
            '>
                🟢 &nbsp;Available for collaboration
            </div>
            <h1 class="hero-title" style='
                font-size: 3.5rem; font-weight: 800;
                line-height: 1.1; margin-bottom: 12px;
            '>
                Hi, I'm <span class="gradient-text">{personal['name']}</span>
            </h1>
            <h3 class="hero-sub" style='
                font-size: 1.35rem; font-weight: 600;
                color: var(--accent-color); margin-bottom: 18px;
                letter-spacing: 0.02em;
            '>
                {personal['role']}
            </h3>
            <p class="hero-desc" style='
                font-size: 1.05rem; color: var(--text-muted);
                line-height: 1.65; margin-bottom: 32px; max-width: 520px;
            '>
                {personal['short_description']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        # CTA buttons
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        with btn_col1:
            if st.button("📂 View My Work", use_container_width=True, type="primary", key="hero_view_work"):
                st.session_state.current_page = "Projects"
                st.rerun()
        with btn_col2:
            st.markdown(
                f'<a href="{personal["github"]}" target="_blank" class="custom-btn-outline"'
                f' style="display:flex;height:38px;align-items:center;justify-content:center;width:100%;">'
                f'🌐 Browse GitHub</a>',
                unsafe_allow_html=True
            )
        with btn_col3:
            resume_path = "assets/resume.pdf"
            resume_data = b"Dinesh Raya - Resume (placeholder). Replace assets/resume.pdf with your real PDF."
            if os.path.exists(resume_path):
                with open(resume_path, "rb") as f:
                    resume_data = f.read()
            st.download_button(
                label="📄 Resume",
                data=resume_data,
                file_name=personal["resume_name"],
                mime="application/pdf",
                use_container_width=True,
                key="resume_download",
            )

    # ── Right: Animated SVG workspace illustration ────────────────────────────
    with col2:
        # Pick fill for screen background based on theme
        screen_fill  = "#050e1a" if theme == "dark" else "#e8edf5"
        card_stroke  = "rgba(79,124,255,0.25)"

        st.markdown(f"""
        <div class="hero-svg-wrap" style="text-align:center; margin-top:10px;">
          <svg viewBox="0 0 480 380" width="100%" height="auto" style="max-width:360px;">
            <!-- Desk surface -->
            <rect x="40" y="310" width="400" height="14" rx="7"
                  fill="var(--border-color)" opacity="0.6"/>

            <!-- Monitor stand -->
            <rect x="218" y="270" width="44" height="40" rx="4"
                  fill="var(--border-color)" opacity="0.7"/>
            <rect x="180" y="308" width="120" height="10" rx="5"
                  fill="var(--border-color)" opacity="0.6"/>

            <!-- Monitor bezel -->
            <rect x="80" y="60" width="320" height="215" rx="14"
                  fill="var(--card-bg)" stroke="{card_stroke}" stroke-width="2"/>
            <!-- Screen -->
            <rect x="94" y="74" width="292" height="185" rx="6"
                  fill="{screen_fill}"/>

            <!-- Editor chrome – title bar dots -->
            <circle cx="112" cy="88" r="5" fill="#FF5F57"/>
            <circle cx="126" cy="88" r="5" fill="#FEBC2E"/>
            <circle cx="140" cy="88" r="5" fill="#28C840"/>

            <!-- Code lines in editor -->
            <rect x="108" y="104" width="55" height="7" rx="3" fill="#4F7CFF" opacity="0.9"/>
            <rect x="108" y="118" width="90" height="6" rx="3" fill="var(--text-muted)" opacity="0.5"/>
            <rect x="120" y="131" width="70" height="6" rx="3" fill="#00D4FF" opacity="0.7"/>
            <rect x="120" y="144" width="50" height="6" rx="3" fill="#a78bfa" opacity="0.7"/>
            <rect x="108" y="157" width="110" height="6" rx="3" fill="var(--text-muted)" opacity="0.4"/>
            <rect x="108" y="170" width="40" height="6" rx="3" fill="#4F7CFF" opacity="0.9"/>
            <rect x="120" y="183" width="80" height="6" rx="3" fill="#00D4FF" opacity="0.7"/>
            <rect x="108" y="196" width="60" height="6" rx="3" fill="var(--text-muted)" opacity="0.5"/>
            <rect x="108" y="209" width="95" height="6" rx="3" fill="#a78bfa" opacity="0.6"/>
            <rect x="108" y="222" width="45" height="6" rx="3" fill="#4F7CFF" opacity="0.9"/>
            <rect x="120" y="235" width="75" height="6" rx="3" fill="var(--text-muted)" opacity="0.4"/>

            <!-- Vertical line numbers gutter -->
            <rect x="94" y="96" width="6" height="185" rx="3" fill="var(--border-color)" opacity="0.5"/>

            <!-- Floating accent bubbles -->
            <circle cx="64"  cy="70"  r="18" fill="#4F7CFF" opacity="0.07"/>
            <circle cx="416" cy="48"  r="28" fill="#00D4FF"  opacity="0.06"/>
            <circle cx="56"  cy="240" r="12" fill="#a78bfa"  opacity="0.08"/>

            <!-- Dashed orbit lines -->
            <path d="M52,78 Q72,38 98,62"
                  stroke="#4F7CFF" stroke-width="1.5" fill="none"
                  opacity="0.25" stroke-dasharray="4,3"/>
            <path d="M392,56 Q418,28 438,52"
                  stroke="#00D4FF" stroke-width="1.5" fill="none"
                  opacity="0.2"  stroke-dasharray="4,3"/>

            <!-- AI brain icon (abstract) -->
            <circle cx="358" cy="148" r="26" fill="var(--card-bg)"
                    stroke="{card_stroke}" stroke-width="1.5"/>
            <circle cx="358" cy="148" r="14" fill="#4F7CFF" opacity="0.25"/>
            <circle cx="358" cy="148" r="6"  fill="#4F7CFF" opacity="0.7"/>
            <line x1="358" y1="122" x2="358" y2="132"
                  stroke="#4F7CFF" stroke-width="1.5" opacity="0.5"/>
            <line x1="358" y1="164" x2="358" y2="174"
                  stroke="#4F7CFF" stroke-width="1.5" opacity="0.5"/>
            <line x1="332" y1="148" x2="342" y2="148"
                  stroke="#4F7CFF" stroke-width="1.5" opacity="0.5"/>
            <line x1="374" y1="148" x2="384" y2="148"
                  stroke="#4F7CFF" stroke-width="1.5" opacity="0.5"/>
          </svg>
        </div>
        """, unsafe_allow_html=True)

    # ── Stats row ─────────────────────────────────────────────────────────────
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='font-size:1.1rem; font-weight:700; color:var(--text-muted); "
        "text-transform:uppercase; letter-spacing:0.08em; margin-bottom:18px;'>"
        "📊 At a Glance</h3>",
        unsafe_allow_html=True
    )

    stats_cols = st.columns(4)
    for i, stat in enumerate(stats):
        with stats_cols[i]:
            st.markdown(f"""
            <div class="stat-card" style="animation-delay:{i*0.12}s;">
                <div style="font-size:1.7rem; margin-bottom:6px;">{stat['icon']}</div>
                <div class="stat-value">{stat['value']}</div>
                <div class="stat-label">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Divider ───────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="
        margin: 50px 0 10px 0;
        height: 1px;
        background: linear-gradient(90deg,
            transparent, var(--border-color), var(--accent-color),
            var(--border-color), transparent);
    "></div>
    """, unsafe_allow_html=True)
