import os
import sys
import sqlite3
import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pipeline.load import DB_PATH, init_db, get_history

st.set_page_config(page_title="GitHub Trending Pipeline", page_icon="", layout="wide")

st.title(" GitHub Trending Pipeline")
st.markdown("Daily snapshots of trending GitHub repos — stars, languages, and trends over time.")

conn = init_db()

history = get_history(conn)
if history.empty:
    st.warning("No data yet. Run `python run_pipeline.py` first.")
    st.stop()

st.subheader("Daily Snapshot Summary")
st.dataframe(history, use_container_width=True, hide_index=True)

st.subheader("Stars Over Time")
fig_data = pd.read_sql(
    "SELECT snapshot_date, full_name, stars FROM repo_snapshots ORDER BY snapshot_date, stars DESC",
    conn
)
if not fig_data.empty:
    pivot = fig_data.pivot_table(index="snapshot_date", columns="full_name", values="stars", aggfunc="max").fillna(0)
    st.line_chart(pivot, height=400)

st.subheader("Top Repos (Latest Snapshot)")
latest_date = history["snapshot_date"].max()
latest = pd.read_sql(
    f"SELECT full_name, owner, stars, forks, language, url FROM repo_snapshots WHERE snapshot_date = '{latest_date}' ORDER BY stars DESC LIMIT 10",
    conn
)
for _, row in latest.iterrows():
    st.markdown(f"**[{row['full_name']}]({row['url']})** — {row['stars']} stars, {row['forks']} forks — {row['language']}")

st.subheader("Language Distribution (Latest)")
lang_data = pd.read_sql(
    f"SELECT language, COUNT(*) as count FROM repo_snapshots WHERE snapshot_date = '{latest_date}' GROUP BY language ORDER BY count DESC",
    conn
)
if not lang_data.empty:
    st.bar_chart(lang_data.set_index("language"))

conn.close()
