from datetime import datetime, timedelta
import requests

GITHUB_API = "https://api.github.com"

def fetch_trending(language: str = "python", since_days: int = 7) -> list[dict]:
    since_date = (datetime.now() - timedelta(days=since_days)).strftime("%Y-%m-%d")
    query = f"language:{language} created:>{since_date}"
    url = f"{GITHUB_API}/search/repositories"
    params = {"q": query, "sort": "stars", "order": "desc", "per_page": 25}
    headers = {"Accept": "application/vnd.github.v3+json"}
    resp = requests.get(url, params=params, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json()["items"]
