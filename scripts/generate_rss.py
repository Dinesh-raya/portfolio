# -*- coding: utf-8 -*-
"""Generate RSS feed XML from portfolio articles.
Run: python scripts/generate_rss.py
Output: assets/feed.xml (deployed alongside the app)
"""
import os
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

from utils.helpers import load_articles


def escape_xml(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_rss() -> str:
    articles = load_articles()
    site_url = "https://github.com/Dinesh-raya/portfolio"

    items = ""
    for art in articles:
        title = escape_xml(art["title"])
        excerpt = escape_xml(art.get("excerpt", ""))
        content = escape_xml(art.get("content", ""))
        pub_date = art.get("date", "")
        try:
            dt = datetime.strptime(pub_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            rfc_date = dt.strftime("%a, %d %b %Y %H:%M:%S +0000")
        except (ValueError, TypeError):
            rfc_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
        link = f"{site_url}/articles/{art.get('filename', '').replace('.md', '')}"
        guid = link

        items += f"""
    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid>{guid}</guid>
      <pubDate>{rfc_date}</pubDate>
      <description>{excerpt}</description>
      <content:encoded><![CDATA[{content}]]></content:encoded>
    </item>"""

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
     xmlns:content="http://purl.org/rss/1.0/modules/content/"
     xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Dinesh Raya — Articles</title>
    <link>{site_url}</link>
    <description>Technical write-ups on AI, Python engineering, and software design by Dinesh Raya.</description>
    <language>en-us</language>
    <lastBuildDate>{datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")}</lastBuildDate>
    <atom:link href="{site_url}/assets/feed.xml" rel="self" type="application/rss+xml"/>
    {items}
  </channel>
</rss>"""


if __name__ == "__main__":
    rss = generate_rss()
    out = os.path.join(ROOT, "assets", "feed.xml")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(rss)
    print(f"RSS feed written to {out}")
