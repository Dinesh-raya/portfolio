# -*- coding: utf-8 -*-
import streamlit as st
import json, os
from data.portfolio_data import PORTFOLIO_DATA
from utils.helpers import error_boundary

@error_boundary
def render_contact() -> None:
    """Render the Contact section with form and details."""
    personal = PORTFOLIO_DATA["personal"]

    st.markdown('<div class="section-header">Contact & Connect</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Have a project idea, collaboration proposal, or just want to say hi? I'd love to hear from you.</p>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1.1, 0.9], gap="large")

    # ── Left: Contact Form ────────────────────────────────────────────────────
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h4 style="color: var(--accent-color); font-weight: 700; font-size: 1.25rem; margin-bottom: 20px;">
                ✉️ Send a Message
            </h4>
        """, unsafe_allow_html=True)

        with st.form("contact_form", clear_on_submit=True):
            name    = st.text_input("Your Name",    placeholder="e.g. Jane Smith",              key="cf_name")
            email   = st.text_input("Your Email",   placeholder="e.g. jane@example.com",        key="cf_email")
            subject = st.text_input("Subject",      placeholder="e.g. Collaboration Proposal",  key="cf_subject")
            message = st.text_area( "Message",      placeholder="Tell me about your project or idea…",
                                    height=140,     key="cf_message")

            submitted = st.form_submit_button("🚀 Send Message", use_container_width=True, type="primary")

        if submitted:
            if name.strip() and email.strip() and message.strip():
                # Persist to messages.json in assets/
                os.makedirs("assets", exist_ok=True)
                msg_path = "assets/messages.json"
                messages = []
                if os.path.exists(msg_path):
                    with open(msg_path, "r") as f:
                        try:
                            messages = json.load(f)
                        except Exception:
                            messages = []
                messages.append({"name": name, "email": email,
                                  "subject": subject, "message": message})
                with open(msg_path, "w") as f:
                    json.dump(messages, f, indent=2)

                st.success(f"✅ Thanks {name}! Your message has been sent. I'll get back to you shortly.")
                st.balloons()
            else:
                st.warning("Please fill in Name, Email, and Message before submitting.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Right: Contact Details ────────────────────────────────────────────────
    with col2:
        # Direct contact cards
        contacts = [
            ("📧", "Email",    personal["email"],    f"mailto:{personal['email']}"),
            ("💼", "LinkedIn", "linkedin.com/in/dineshraya", personal["linkedin"]),
            ("🐙", "GitHub",   "github.com/dineshraya",      personal["github"]),
            ("📍", "Location", personal["location"],  "#"),
        ]

        for icon, label, value, link in contacts:
            href = f'href="{link}" target="_blank"' if link != "#" else ""
            cursor = "pointer" if link != "#" else "default"
            st.markdown(f"""
            <a {href} style="text-decoration: none;">
                <div class="glass-card" style="display: flex; align-items: center; gap: 16px;
                                                cursor: {cursor}; margin-bottom: 12px;">
                    <div style="font-size: 1.6rem; min-width: 40px; text-align: center;">{icon}</div>
                    <div>
                        <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.06em;
                                    color: var(--text-muted); font-weight: 600; margin-bottom: 2px;">{label}</div>
                        <div style="font-weight: 600; color: var(--text-color); font-size: 0.95rem;">{value}</div>
                    </div>
                </div>
            </a>
            """, unsafe_allow_html=True)

        # Availability badge
        st.markdown("""
        <div class="glass-card" style="text-align: center; margin-top: 8px; padding: 20px;">
            <div style="display: inline-flex; align-items: center; gap: 8px;
                         background: rgba(0, 212, 100, 0.12); border: 1px solid rgba(0,212,100,0.25);
                         border-radius: 30px; padding: 8px 18px; font-size: 0.9rem;
                         font-weight: 600; color: #00d464;">
                <span style="width: 9px; height: 9px; border-radius: 50%; background: #00d464;
                              display: inline-block; animation: pulse 2s infinite;"></span>
                Available for freelance & collaboration
            </div>
        </div>
        <style>
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50%       { opacity: 0.4; }
        }
        </style>
        """, unsafe_allow_html=True)
