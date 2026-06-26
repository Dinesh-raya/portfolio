import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Code Review", page_icon="", layout="wide")

st.title(" AI Code Review")
st.markdown("Paste your code and get an AI-powered review — bugs, security, style, and performance.")

col1, col2 = st.columns([0.7, 0.3])

with col2:
    language = st.selectbox("Language", ["python", "javascript", "typescript", "java", "go", "rust", "cpp", "csharp", "ruby", "php"])
    focus = st.radio("Focus area", ["all", "bugs", "security", "performance", "style"], index=0)

with col1:
    code = st.text_area("Paste your code here", height=400, placeholder="def hello():\n    print('world')")

if st.button("Review Code", type="primary", use_container_width=True):
    if not code.strip():
        st.warning("Paste some code first.")
        st.stop()

    with st.spinner("Reviewing..."):
        try:
            resp = requests.post(
                f"{API_URL}/review",
                json={"code": code, "language": language, "focus": focus},
                timeout=30,
            )
            if resp.ok:
                data = resp.json()
                st.success(f"Review complete — {data['line_count']} lines reviewed")
                st.markdown(data["feedback"])
            else:
                st.error(resp.json().get("detail", "Review failed"))
        except Exception as e:
            st.error(f"Could not reach API: {e}")
            st.info("Make sure the backend is running and API_URL is set correctly.")
