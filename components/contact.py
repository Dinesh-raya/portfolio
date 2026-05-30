# -*- coding: utf-8 -*-
import streamlit as st
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary, send_contact_form

@error_boundary
def render_contact() -> None:
    """Render the Contact section with form and details."""
    personal = PORTFOLIO_DATA["personal"]
    gh_user = personal.get("github_username", "Dinesh-raya")

    st.markdown('<div class="section-header">Contact & Connect</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Have a project idea, collaboration proposal, or just want to say hi? I'd love to hear from you.</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    with col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.25rem; margin-bottom: 20px;">
                Send a Message
            </h4>
        """, unsafe_allow_html=True)

        with st.form("contact_form", clear_on_submit=True):
            name = st.text_input("Your Name", placeholder="e.g. Jane Smith", key="cf_name")
            email = st.text_input("Your Email", placeholder="e.g. jane@example.com", key="cf_email")
            subject = st.text_input("Subject", placeholder="e.g. Collaboration Proposal", key="cf_subject")
            message = st.text_area(
                "Message",
                placeholder="Tell me about your project or idea (min 20 characters)...",
                height=140,
                key="cf_message",
            )
            st.caption(f"{len(st.session_state.get('cf_message', '') or '')} characters")
            submitted = st.form_submit_button("Send Message", width="stretch", type="primary")

        if submitted:
            with st.spinner("Sending..."):
                ok, msg = send_contact_form(name, email, subject, message, source="contact_page")
            if ok:
                st.success(msg)
                st.balloons()
            else:
                st.error(msg)
                st.markdown(f"**Or email me directly:** [{personal['email']}](mailto:{personal['email']})")

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        contacts = [
            ("Email", personal["email"], f"mailto:{personal['email']}"),
            ("LinkedIn", f"linkedin.com/in/{personal['linkedin'].rstrip('/').split('/')[-1]}", personal["linkedin"]),
            ("GitHub", f"github.com/{gh_user}", personal["github"]),
            ("Location", personal["location"], "#"),
        ]

        for label, value, link in contacts:
            href = f'href="{link}" target="_blank"' if link != "#" else ""
            cursor = "pointer" if link != "#" else "default"
            st.markdown(f"""
            <a {href} style="text-decoration: none;">
                <div class="glass-card" style="display: flex; align-items: center; gap: 16px;
                                                cursor: {cursor}; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em;
                                    color: var(--text-muted); font-weight: 600; margin-bottom: 2px;">{label}</div>
                        <div style="font-weight: 600; color: var(--text-color); font-size: 0.95rem;">{value}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card" style="text-align: center; margin-top: 8px; padding: 20px;">
            <div style="display: inline-flex; align-items: center; gap: 8px;
                         background: rgba(0, 212, 100, 0.12); border: 1px solid rgba(0,212,100,0.25);
                         border-radius: 30px; padding: 8px 18px; font-size: 0.9rem;
                         font-weight: 600; color: var(--color-success);">
                <span class="status-dot"></span>
                Available for freelance and collaboration
            </div>
        </div>
        """, unsafe_allow_html=True)
