# -*- coding: utf-8 -*-
"""Live browser check: screenshots + assertions."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "scripts", "screenshots")
BASE = os.environ.get("PORTFOLIO_URL", "http://localhost:8501")

FAILURES: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    status = "PASS" if ok else "FAIL"
    msg = f"[{status}] {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    if not ok:
        FAILURES.append(name)


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("[FAIL] playwright not installed")
        return 1

    pages_to_test = [
        ("home", 0, ["Skills Snapshot", "Featured Projects", "Let's Connect"]),
        ("about", 1, ["About Me", "engineering"]),
        ("projects", 2, ["Projects"]),
    ]

    print(f"=== Live check @ {BASE} ===\n")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        try:
            page.goto(BASE, wait_until="domcontentloaded", timeout=60000)
        except Exception as exc:
            print(f"[FAIL] Could not load app: {exc}")
            browser.close()
            return 1

        page.wait_for_timeout(8000)
        text = page.inner_text("body")

        if "ImportError" in text or "Traceback" in text:
            check("no import/runtime error", False, text[:200].replace("\n", " "))
        else:
            check("no import/runtime error", True)

        check("server responds", len(text) > 300, f"{len(text)} chars visible")
        check("name rendered", "Dinesh Raya" in text)
        check("no HTML leak", "font-size: 1.15rem; font-weight: 700" not in text)
        check("no SVG source leak", "<!-- Monitor" not in text)

        path_home = os.path.join(OUT, "01_home.png")
        page.screenshot(path=path_home, full_page=True)
        print(f"  screenshot: {path_home}")

        nav_links = page.locator('[data-testid="stSidebar"] a')
        n_nav = nav_links.count()
        check("sidebar nav links", n_nav >= 3, f"found {n_nav} clickable links")

        for slug, index, keywords in pages_to_test:
            if index < n_nav:
                nav_links.nth(index).click()
                page.wait_for_timeout(3500)
                body = page.inner_text("body").lower()
                hit = any(k.lower() in body for k in keywords)
                check(f"page '{slug}'", hit, f"keywords={keywords}")
                shot = os.path.join(OUT, f"02_{slug}.png" if slug != "home" else "01_home_nav.png")
                if slug != "home":
                    page.screenshot(path=shot, full_page=True)
                    print(f"  screenshot: {shot}")

        browser.close()

    print()
    if FAILURES:
        print("FAILED:", ", ".join(FAILURES))
        return 1
    print("Live check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
