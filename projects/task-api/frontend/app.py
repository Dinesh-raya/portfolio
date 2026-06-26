import os
import requests
import streamlit as st

API_BASE = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Task Manager", page_icon="", layout="centered")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = ""

def api(method: str, path: str, **kwargs):
    headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
    return requests.request(method, f"{API_BASE}{path}", headers=headers, **kwargs, timeout=15)

st.title(" Task Manager")

if not st.session_state.token:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Login"):
            resp = api("POST", "/auth/login", json={"username": u, "password": p})
            if resp.ok:
                st.session_state.token = resp.json()["token"]
                st.session_state.username = u
                st.rerun()
            else:
                st.error(resp.json().get("detail", "Login failed"))
    with tab2:
        u = st.text_input("Username", key="reg_u")
        p = st.text_input("Password", type="password", key="reg_p")
        if st.button("Register"):
            resp = api("POST", "/auth/register", json={"username": u, "password": p})
            if resp.ok:
                st.session_state.token = resp.json()["token"]
                st.session_state.username = u
                st.rerun()
            else:
                st.error(resp.json().get("detail", "Registration failed"))
    st.stop()

st.success(f"Logged in as **{st.session_state.username}**")
if st.button("Logout"):
    st.session_state.token = None
    st.session_state.username = ""
    st.rerun()

st.divider()

with st.form("new_task"):
    title = st.text_input("Task title")
    desc = st.text_area("Description (optional)")
    if st.form_submit_button("Add Task") and title:
        api("POST", "/tasks", json={"title": title, "description": desc})
        st.rerun()

st.divider()
st.subheader("Your Tasks")

tasks = api("GET", "/tasks").json()
if not tasks:
    st.info("No tasks yet. Create one above.")

for t in tasks:
    col1, col2, col3 = st.columns([0.05, 0.7, 0.25])
    with col1:
        checked = st.checkbox("", value=t["completed"], key=f"chk_{t['id']}")
        if checked != t["completed"]:
            api("PATCH", f"/tasks/{t['id']}", json={"completed": checked})
            st.rerun()
    with col2:
        title_display = f"~~{t['title']}~~" if t["completed"] else t["title"]
        st.markdown(f"**{title_display}**")
        if t["description"]:
            st.caption(t["description"])
    with col3:
        if st.button("Delete", key=f"del_{t['id']}"):
            api("DELETE", f"/tasks/{t['id']}")
            st.rerun()
