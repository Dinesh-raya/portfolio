# -*- coding: utf-8 -*-
import streamlit as st
import textwrap
from utils.helpers import error_boundary

# ── helper: mock AI responses ────────────────────────────────────────────────
_CHAT_RESPONSES = {
    "hello":      "Hello! I'm Dinesh's AI assistant. Ask me anything about his projects, skills, or experience. 👋",
    "project":    "Dinesh has built AI PDF Analyzers, Resume Screeners, Automation Dashboards, and more. Check the Projects section for full details! 🚀",
    "skill":      "Core skills: Python, AI/ML (LLMs, RAG), Streamlit, Data Structures & Algorithms, Docker, and SQL. 💡",
    "contact":    "You can reach Dinesh via the Contact section below or directly at dineshraya.dev@gmail.com 📧",
    "experience": "Dinesh has 3+ years of learning & building — from algorithms to full AI-powered products. 🏗️",
    "default":    "Great question! Dinesh focuses on building intelligent, practical AI & Python solutions. Feel free to explore the portfolio sections for more. 🔍",
}

def _mock_chat(msg: str) -> str:
    m = msg.lower()
    for key, reply in _CHAT_RESPONSES.items():
        if key in m:
            return reply
    return _CHAT_RESPONSES["default"]


# ── helper: prompt optimizer ──────────────────────────────────────────────────
def _optimize_prompt(raw: str) -> str:
    return textwrap.dedent(f"""
    **Role:** You are an expert AI assistant specialised in [domain].

    **Context:** {raw.strip()}

    **Task:** Provide a clear, structured, and detailed response that:
    - Addresses the core question directly
    - Includes relevant examples where applicable
    - Offers actionable next steps

    **Constraints:**
    - Be concise but thorough
    - Use professional language
    - Format with headers and bullet points where appropriate

    **Output format:** Markdown
    """).strip()


# ── helper: Python code analyser ─────────────────────────────────────────────
def _analyse_code(code: str) -> str:
    issues = []
    lines = code.split("\n")

    if len(lines) > 1 and not any(l.startswith("def ") or l.startswith("class ") for l in lines):
        issues.append("💡 **Modularity**: Consider wrapping logic in functions or classes for reusability.")
    if "print(" in code and "logging" not in code:
        issues.append("💡 **Logging**: Replace `print()` with Python's `logging` module for production-grade output.")
    if "except:" in code:
        issues.append("⚠️ **Bare except**: Avoid bare `except:` — catch specific exception types (e.g. `except ValueError:`).")
    if "import *" in code:
        issues.append("⚠️ **Wildcard import**: Avoid `import *` — it pollutes the namespace and hampers readability.")
    if not any(l.strip().startswith("#") for l in lines):
        issues.append("📝 **Comments**: Add inline comments to document intent, especially for non-obvious logic.")

    if not issues:
        return "✅ **No major issues detected.** Code looks clean and follows good practices."
    return "\n\n".join(issues)


# ── main render ───────────────────────────────────────────────────────────────
@error_boundary
def render_playground():
    st.markdown('<div class="section-header">Interactive Playground</div>', unsafe_allow_html=True)
    st.markdown(
        "<p style='color: var(--text-muted); font-size: 1.1rem; margin-bottom: 30px;'>"
        "Mini AI utilities — interactive, practical, and built to demonstrate real engineering thinking.</p>",
        unsafe_allow_html=True
    )

    tab_chat, tab_pdf, tab_prompt, tab_code = st.tabs([
        "🤖 AI Assistant",
        "📄 PDF Summariser",
        "✨ Prompt Optimizer",
        "🔍 Code Analyser",
    ])

    # ── Tab 1: AI Chatbot ─────────────────────────────────────────────────────
    with tab_chat:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">🤖 Portfolio AI Assistant</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Ask anything about Dinesh's skills, projects, or background.
                This assistant is a smart mock — no API key needed!
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Initialise chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hi there! 👋 I'm Dinesh's portfolio assistant. What would you like to know?"}
            ]

        # Render existing messages
        for msg in st.session_state.chat_history:
            css_class = "chat-user" if msg["role"] == "user" else "chat-assistant"
            align = "flex-end" if msg["role"] == "user" else "flex-start"
            st.markdown(f"""
            <div style="display: flex; justify-content: {align}; margin-bottom: 10px;">
                <div class="chat-bubble {css_class}">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Input
        user_input = st.chat_input("Ask about projects, skills, experience…", key="playground_chat")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            reply = _mock_chat(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.rerun()

        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Chat cleared! How can I help you? 👋"}
            ]
            st.rerun()

    # ── Tab 2: PDF Summariser ────────────────────────────────────────────────
    with tab_pdf:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">📄 PDF Summariser</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Upload any PDF document and get a structured extraction of its key points and structure.
                (Simulation mode — no external API required.)
            </p>
        </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"], key="pdf_upload")

        if uploaded_file:
            file_size_kb = len(uploaded_file.getvalue()) / 1024
            st.markdown(f"""
            <div class="glass-card" style="margin: 20px 0;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="font-size: 2.2rem;">📑</div>
                    <div>
                        <div style="font-weight: 700; color: var(--text-color);">{uploaded_file.name}</div>
                        <div style="color: var(--text-muted); font-size: 0.88rem;">{file_size_kb:.1f} KB uploaded</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔍 Analyse Document", key="analyse_pdf", type="primary"):
                with st.spinner("Extracting and analysing document structure…"):
                    import time; time.sleep(1.5)

                st.success("✅ Analysis complete!")
                st.markdown("""
                <div class="glass-card">
                    <h5 style="color: var(--accent-color); font-weight: 700; margin-bottom: 14px;">📋 Document Summary</h5>
                    <ul style="color: var(--text-muted); font-size: 0.95rem; line-height: 1.7; padding-left: 20px;">
                        <li>Document contains structured sections with clear headings.</li>
                        <li>Key topics identified: AI/ML, Software Engineering, Data Systems.</li>
                        <li>Estimated reading time: 8–12 minutes.</li>
                        <li>Document appears technical in nature — suitable for developer audience.</li>
                    </ul>
                    <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 12px; font-style: italic;">
                        ℹ️ This is a simulation. In a production version, text extraction
                        via PyMuPDF/pdfplumber + LLM summarisation would be used.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 50px 20px; color: var(--text-muted); font-size: 0.95rem;">
                <div style="font-size: 3rem; margin-bottom: 14px;">📂</div>
                Drop a PDF above to get started.
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Prompt Optimizer ──────────────────────────────────────────────
    with tab_prompt:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">✨ LLM Prompt Optimizer</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Enter a raw, vague prompt and instantly receive a structured, professional version
                following Role → Context → Task → Constraints format.
            </p>
        </div>
        """, unsafe_allow_html=True)

        raw_prompt = st.text_area(
            "Enter your rough prompt:",
            placeholder="e.g. Write me a summary of machine learning…",
            height=130,
            key="raw_prompt_input"
        )

        if st.button("⚡ Optimise Prompt", key="optimise_btn", type="primary"):
            if raw_prompt.strip():
                optimised = _optimize_prompt(raw_prompt)
                st.markdown("""
                <div style="margin-top: 20px;">
                    <h5 style="color: var(--accent-color); font-weight: 700; margin-bottom: 10px;">
                        🎯 Optimised Prompt
                    </h5>
                </div>
                """, unsafe_allow_html=True)
                st.code(optimised, language="markdown")
                st.success("✅ Prompt optimised! Copy and paste this into any LLM.")
            else:
                st.warning("Please enter a prompt to optimise.")

    # ── Tab 4: Code Analyser ─────────────────────────────────────────────────
    with tab_code:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">🔍 Python Code Analyser</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Paste Python code below and receive instant static-analysis feedback covering
                best practices, logging, exception handling, and modularity.
            </p>
        </div>
        """, unsafe_allow_html=True)

        default_code = '''def process(data):
    try:
        result = [x * 2 for x in data]
        print("Done:", result)
        return result
    except:
        print("Error occurred")
'''

        code_input = st.text_area(
            "Paste your Python code:",
            value=default_code,
            height=220,
            key="code_analyser_input"
        )

        if st.button("🔎 Analyse Code", key="analyse_code_btn", type="primary"):
            if code_input.strip():
                with st.spinner("Running static analysis…"):
                    import time; time.sleep(0.8)
                analysis = _analyse_code(code_input)
                st.markdown("""
                <div style="margin-top: 20px;">
                    <h5 style="color: var(--accent-color); font-weight: 700; margin-bottom: 10px;">
                        📊 Analysis Report
                    </h5>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="glass-card">
                    {analysis.replace(chr(10), "<br>")}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please paste some Python code to analyse.")
