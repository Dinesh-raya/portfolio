# -*- coding: utf-8 -*-
"""Browser smoke test — requires Streamlit running (default http://localhost:8501)."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

BASE = os.environ.get("PORTFOLIO_URL", "http://localhost:8502")
FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    line = f"[{status}] UI: {name}"
    if detail:
        line += f" — {detail}"
    print(line)
    if not ok:
        FAILURES.append(name)


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[SKIP] UI: playwright not installed")
        return 0

    print(f"=== UI verification @ {BASE} ===\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        try:
            page.goto(BASE, wait_until="domcontentloaded", timeout=60000)
        except Exception as exc:
            print(f"[FAIL] UI: could not load {BASE} — {exc}")
            print("Start the app: streamlit run app.py")
            browser.close()
            return 1

        page.wait_for_timeout(4000)
        text = page.inner_text("body")

        check("app loads body", len(text) > 200, f"{len(text)} chars")
        check("name visible", "Dinesh Raya" in text)
        check("no raw sidebar HTML leak", "font-size: 1.15rem; font-weight: 700" not in text)
        check("no raw SVG leak", "<!-- Monitor" not in text and "Scatterpolar" not in text)
        check("dashboard hero", "Hi, I'm" in text or "Hi, I" in text)
        check("skills snapshot", "Skills Snapshot" in text)
        check("featured projects", "Featured Projects" in text)
        check("experience section", "Experience" in text)
        check("contact form area", "Let's Connect" in text or "Send Message" in text)

        # Optional: click second nav item (About) if option_menu rendered
        nav_links = page.locator('[data-testid="stSidebar"] a')
        if nav_links.count() >= 2:
            nav_links.nth(1).click()
            page.wait_for_timeout(2500)
            body_after = page.inner_text("body")
            navigated = "About Me" in body_after or "engineering background" in body_after.lower()
            check("page navigation", navigated, f"{nav_links.count()} sidebar links")
        else:
            print("[WARN] UI: page navigation — sidebar links not clickable in headless mode")

        browser.close()

    print()
    if FAILURES:
        print(f"UI FAILED: {', '.join(FAILURES)}")
        return 1
    print("UI smoke tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
