# -*- coding: utf-8 -*-
import streamlit as st
import textwrap
import re
import ast
import time
from utils.helpers import error_boundary

# ── helper: expanded AI chat responses ──────────────────────────────────────
_CHAT_RESPONSES = {
    # Greetings
    "hello": "Hello! I'm Dinesh's AI assistant. Ask me about his projects, skills, experience, or tech stack.",
    "hi": "Hey there! What would you like to know about Dinesh's work?",
    "hey": "Hi! Feel free to ask about projects, skills, or experience.",
    # Projects
    "project": "Dinesh has built 15+ projects including AI PDF Analyzers, Resume Screeners, Automation Dashboards, and this portfolio. The Projects section has full details with GitHub links.",
    "projects": "Key projects: AI PDF Analyzer (PyMuPDF + NLP), Resume Screener (skill extraction), Streamlit Portfolio (this site!), and multiple automation scripts. Want details on any specific one?",
    # Skills
    "skill": "Core skills: Python, AI/ML (LLMs, RAG, NLP), Streamlit, Data Structures & Algorithms, Docker, SQL, Git, and Linux.",
    "skills": "Technical skills span 6 domains: AI/ML, Web Development, Data Engineering, DevOps, Automation, and Software Design. The Skills page has a radar chart breakdown.",
    "tech": "Tech stack includes Python, Streamlit, PyTorch, scikit-learn, Pandas, Docker, PostgreSQL, FastAPI, Git, and Linux.",
    # Experience
    "experience": "Dinesh has 3+ years of hands-on learning and building — from algorithm design to full AI-powered products. Check the Experience section for timeline details.",
    "work": "Work experience spans AI development, Python engineering, and automation. Built production-grade tools and dashboards.",
    # Contact
    "contact": "You can reach Dinesh via the Contact section or directly at dineshraya365@gmail.com. Also available on LinkedIn and GitHub.",
    "email": "Best way to reach Dinesh: dineshraya365@gmail.com or use the contact form on this portfolio.",
    "hire": "Dinesh is available for freelance and collaboration! Use the Contact section to get in touch.",
    # AI/ML specific
    "ai": "Dinesh works with LLMs, RAG pipelines, NLP, prompt engineering, and ML model deployment. He's passionate about making AI practical and accessible.",
    "machine learning": "ML experience includes PyTorch, scikit-learn, data preprocessing, model evaluation, and deploying models via Streamlit and FastAPI.",
    "llm": "Experience with Large Language Models includes RAG pipeline design, prompt optimization, context window management, and building AI-powered applications.",
    "rag": "RAG (Retrieval-Augmented Generation) expertise: query expansion, multi-vector indexing, re-ranking strategies, and evaluation frameworks.",
    # Python
    "python": "Python is the primary language — used for AI/ML, web apps, automation, data processing, and scripting. 3+ years of daily use.",
    "streamlit": "This portfolio is built with Streamlit! Dinesh has deep experience with custom theming, session state management, and responsive layouts.",
    # Default
    "default": "Great question! Dinesh focuses on building intelligent, practical AI & Python solutions. Try asking about projects, skills, experience, or tech stack.",
}

_SUGGESTED_QUESTIONS = {
    "default": ["What projects has Dinesh built?", "What are his core skills?", "How can I contact him?"],
    "project": ["What tech stack does he use?", "Tell me about his AI projects", "What's his experience?"],
    "projects": ["What tech stack does he use?", "Tell me about his AI projects", "What's his experience?"],
    "skill": ["What AI/ML frameworks?", "What about Python?", "Tell me about his projects"],
    "skills": ["What AI/ML frameworks?", "What about Python?", "Tell me about his projects"],
    "experience": ["What has he built?", "What's his tech stack?", "How can I contact him?"],
    "work": ["What has he built?", "What's his tech stack?", "How can I contact him?"],
    "contact": ["What projects has he built?", "Is he available for hire?", "What are his skills?"],
    "email": ["What projects has he built?", "Is he available for hire?", "What are his skills?"],
    "hire": ["What projects has he built?", "What are his skills?", "How can I contact him?"],
    "ai": ["Tell me about RAG pipelines", "What ML frameworks?", "What projects use AI?"],
    "machine learning": ["Tell me about RAG pipelines", "What AI projects?", "What's his tech stack?"],
    "llm": ["Tell me about RAG pipelines", "What AI projects?", "What ML frameworks?"],
    "rag": ["What other AI work?", "What ML frameworks?", "What projects use this?"],
    "python": ["What about Streamlit?", "What projects use Python?", "What AI/ML work?"],
    "streamlit": ["What other tech?", "Tell me about this portfolio", "What projects has he built?"],
}


def _mock_chat(msg: str) -> tuple:
    """Return (response, suggested_questions) based on keywords."""
    m = msg.lower()
    for key, reply in _CHAT_RESPONSES.items():
        if key in m:
            suggestions = _SUGGESTED_QUESTIONS.get(key, _SUGGESTED_QUESTIONS["default"])
            return reply, suggestions
    return _CHAT_RESPONSES["default"], _SUGGESTED_QUESTIONS["default"]


# ── helper: PDF text extraction ─────────────────────────────────────────────
def _extract_pdf_info(uploaded_file) -> dict:
    """Extract real metadata and text from an uploaded PDF."""
    import fitz  # PyMuPDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    pages = len(doc)
    full_text = ""
    headings = []

    for page in doc:
        page_text = page.get_text()
        full_text += page_text + "\n"

        # Detect headings (text with larger font or bold)
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] > 14 or (span["flags"] & 2**4):  # bold flag
                            text = span["text"].strip()
                            if text and len(text) > 2 and len(text) < 100:
                                headings.append(text)

    words = len(full_text.split())
    paragraphs = len([p for p in full_text.split("\n\n") if p.strip()])
    sentences = len(re.split(r'[.!?]+', full_text))
    reading_time = max(1, words // 200)

    doc.close()

    return {
        "pages": pages,
        "words": words,
        "paragraphs": paragraphs,
        "sentences": sentences,
        "reading_time": reading_time,
        "headings": headings[:20],
        "preview": full_text[:500],
    }


# ── helper: domain-aware prompt optimizer ───────────────────────────────────
_DOMAIN_TEMPLATES = {
    "coding": {
        "keywords": ["code", "function", "api", "debug", "program", "script", "python", "javascript", "bug", "error"],
        "prefix": "You are a senior software engineer.",
        "improvements": ["Added error handling requirements", "Specified language/framework context"],
    },
    "writing": {
        "keywords": ["write", "essay", "article", "blog", "content", "copy", "story", "paragraph"],
        "prefix": "You are an expert writer and editor.",
        "improvements": ["Specified tone and audience", "Added word count guidance"],
    },
    "analysis": {
        "keywords": ["analyze", "data", "compare", "evaluate", "research", "metrics", "report", "statistics"],
        "prefix": "You are a data analyst expert.",
        "improvements": ["Specified data format", "Added methodology constraints"],
    },
    "creative": {
        "keywords": ["design", "creative", "brainstorm", "idea", "innovate", "imagine", "concept"],
        "prefix": "You are a creative director.",
        "improvements": ["Added brand constraints", "Specified target audience"],
    },
    "academic": {
        "keywords": ["explain", "theory", "concept", "research", "paper", "study", "academic", "science"],
        "prefix": "You are an academic researcher.",
        "improvements": ["Added citation requirements", "Specified complexity level"],
    },
}

_OUTPUT_FORMATS = {
    "table": "Format your response as a markdown table.",
    "list": "Format your response as a numbered list.",
    "code": "Include code examples in your response.",
    "markdown": "Use markdown formatting with headers and bullet points.",
    "step": "Provide step-by-step instructions.",
}


def _optimize_prompt(raw: str) -> tuple:
    """Detect domain and optimize the prompt. Returns (optimized, improvements_applied)."""
    m = raw.lower()
    domain = "coding"  # default
    for d, info in _DOMAIN_TEMPLATES.items():
        if any(kw in m for kw in info["keywords"]):
            domain = d
            break

    template = _DOMAIN_TEMPLATES[domain]
    improvements = []

    optimized = f"**Role:** {template['prefix']}\n\n"
    optimized += f"**Context:** {raw.strip()}\n\n"
    optimized += "**Task:** Provide a clear, structured response that:\n"
    optimized += "- Addresses the core question directly\n"
    optimized += "- Includes relevant examples\n"
    optimized += "- Offers actionable next steps\n"

    # Detect output format
    for fmt, instruction in _OUTPUT_FORMATS.items():
        if fmt in m:
            optimized += f"\n**Format:** {instruction}\n"
            improvements.append(f"Added {fmt} format instruction")
            break

    improvements.extend(template["improvements"][:2])

    optimized += "\n**Constraints:** Be concise but thorough. Use professional language."

    return optimized, improvements


# ── helper: AST code analyzer ───────────────────────────────────────────────
def _analyze_code(code_str: str) -> dict:
    """Analyze Python code using AST. Returns metrics and issues."""
    issues = []
    metrics = {
        "lines": len(code_str.split("\n")),
        "functions": 0,
        "classes": 0,
        "imports": 0,
        "has_type_hints": False,
        "has_docstrings": False,
        "bare_excepts": 0,
        "complexity": 0,
    }

    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {"error": f"Syntax Error: {e}", "metrics": metrics, "issues": [str(e)], "score": 0}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            metrics["functions"] += 1
            # Check type hints
            if node.returns or any(arg.annotation for arg in node.args.args):
                metrics["has_type_hints"] = True
            # Check docstrings
            if (node.body and isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, (ast.Constant, ast.Str))):
                metrics["has_docstrings"] = True
            # Check naming convention
            if not node.name.islower() and "_" not in node.name:
                issues.append(f"Function '{node.name}' should use snake_case")

        elif isinstance(node, ast.ClassDef):
            metrics["classes"] += 1

        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            metrics["imports"] += 1

        elif isinstance(node, ast.ExceptHandler) and node.type is None:
            metrics["bare_excepts"] += 1
            issues.append("Bare except clause detected — specify exception type")

    # Complexity estimate (simplified)
    complexity_nodes = (ast.If, ast.For, ast.While, ast.Try, ast.With, ast.BoolOp)
    metrics["complexity"] = sum(1 for _ in ast.walk(tree) if isinstance(_, complexity_nodes))

    # Calculate score
    score = 100
    if metrics["bare_excepts"] > 0:
        score -= metrics["bare_excepts"] * 10
    if not metrics["has_type_hints"]:
        score -= 15
    if not metrics["has_docstrings"]:
        score -= 10
    if metrics["complexity"] > 20:
        score -= 10
    score = max(0, min(100, score))

    return {"metrics": metrics, "issues": issues, "score": score}


# ── main render ───────────────────────────────────────────────────────────────
@error_boundary
def render_playground() -> None:
    """Render the Interactive Playground with AI tools."""
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
                This assistant uses smart pattern matching — no API key needed!
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Initialise chat history
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Hi there! I'm Dinesh's portfolio assistant. What would you like to know?"}
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
        user_input = st.chat_input("Ask about projects, skills, experience...", key="playground_chat")
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                time.sleep(0.5)  # Brief typing animation
                reply, suggestions = _mock_chat(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.session_state.pending_suggestions = suggestions
            st.rerun()

        # Suggested follow-up questions
        suggestions = st.session_state.get("pending_suggestions", _SUGGESTED_QUESTIONS["default"])
        if suggestions:
            st.markdown("**Try asking:**")
            cols = st.columns(len(suggestions))
            for i, q in enumerate(suggestions):
                if cols[i].button(q, key=f"suggest_{i}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": q})
                    with st.spinner("Thinking..."):
                        time.sleep(0.5)
                        response, new_suggestions = _mock_chat(q)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    st.session_state.pending_suggestions = new_suggestions
                    st.rerun()

        if st.button("🗑️ Clear Chat", key="clear_chat"):
            st.session_state.chat_history = [
                {"role": "assistant", "content": "Chat cleared! How can I help you?"}
            ]
            st.session_state.pending_suggestions = _SUGGESTED_QUESTIONS["default"]
            st.rerun()

    # ── Tab 2: PDF Summariser ────────────────────────────────────────────────
    with tab_pdf:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">📄 PDF Summariser</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Upload any PDF document and get real text extraction, page count, and document structure.
            </p>
        </div>
        """, unsafe_allow_html=True)

        pdf_file = st.file_uploader("Upload a PDF document", type=["pdf"], key="pdf_upload")

        if pdf_file:
            file_size_kb = len(pdf_file.getvalue()) / 1024
            st.markdown(f"""
            <div class="glass-card" style="margin: 20px 0;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div style="font-size: 2.2rem;">📑</div>
                    <div>
                        <div style="font-weight: 700; color: var(--text-color);">{pdf_file.name}</div>
                        <div style="color: var(--text-muted); font-size: 0.88rem;">{file_size_kb:.1f} KB uploaded</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("🔍 Analyse Document", key="analyse_pdf", type="primary"):
                with st.spinner("Extracting text and structure..."):
                    info = _extract_pdf_info(pdf_file)

                st.success("Analysis complete!")

                # Metrics row
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Pages", info["pages"])
                col2.metric("Words", f"{info['words']:,}")
                col3.metric("Paragraphs", info["paragraphs"])
                col4.metric("Reading Time", f"{info['reading_time']} min")

                # Document structure
                if info["headings"]:
                    st.markdown("**Document Structure:**")
                    for h in info["headings"]:
                        st.markdown(f"- {h}")

                # Text preview
                with st.expander("Text Preview (first 500 chars)"):
                    st.text(info["preview"])
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
                Enter a raw prompt and get a domain-aware optimized version with before/after comparison.
            </p>
        </div>
        """, unsafe_allow_html=True)

        raw_prompt = st.text_area(
            "Enter your rough prompt:",
            placeholder="e.g. Write me a summary of machine learning...",
            height=130,
            key="raw_prompt_input"
        )

        if st.button("⚡ Optimise Prompt", key="optimise_btn", type="primary"):
            if raw_prompt.strip():
                optimized, improvements = _optimize_prompt(raw_prompt)

                # Before/After comparison
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Before:**")
                    st.code(raw_prompt, language="text")
                with col2:
                    st.markdown("**After:**")
                    st.code(optimized, language="markdown")

                if improvements:
                    st.markdown("**Improvements applied:**")
                    for imp in improvements:
                        st.markdown(f"- {imp}")

                st.success("Prompt optimized! Copy and paste this into any LLM.")
            else:
                st.warning("Please enter a prompt to optimize.")

    # ── Tab 4: Code Analyser ─────────────────────────────────────────────────
    with tab_code:
        st.markdown("""
        <div class="glass-card" style="margin-bottom: 20px;">
            <h4 style="color: var(--accent-color); font-weight: 700; margin-bottom: 8px;">🔍 Python Code Analyser</h4>
            <p style="color: var(--text-muted); font-size: 0.95rem; margin: 0;">
                Paste Python code below for real AST-based static analysis with quality scoring.
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
                with st.spinner("Running static analysis..."):
                    result = _analyze_code(code_input)

                if "error" in result:
                    st.error(result["error"])
                else:
                    # Score display
                    score = result["score"]
                    color = "#00d464" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
                    st.markdown(f'<div style="text-align:center; font-size:3rem; font-weight:800; color:{color};">{score}/100</div>', unsafe_allow_html=True)
                    st.markdown('<div style="text-align:center; color:var(--text-muted); margin-bottom:20px;">Code Quality Score</div>', unsafe_allow_html=True)

                    # Metrics
                    m = result["metrics"]
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Lines", m["lines"])
                    col2.metric("Functions", m["functions"])
                    col3.metric("Classes", m["classes"])
                    col4.metric("Complexity", m["complexity"])

                    # Issues
                    if result["issues"]:
                        st.markdown("**Issues Found:**")
                        for issue in result["issues"]:
                            st.warning(issue)
                    else:
                        st.success("No issues found!")
            else:
                st.warning("Please paste some Python code to analyse.")
