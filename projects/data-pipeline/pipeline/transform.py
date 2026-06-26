import pandas as pd

def transform_repos(raw: list[dict]) -> pd.DataFrame:
    rows = []
    for r in raw:
        rows.append({
            "full_name": r["full_name"],
            "owner": r["owner"]["login"],
            "description": (r["description"] or "")[:200],
            "stars": r["stargazers_count"],
            "forks": r["forks_count"],
            "open_issues": r["open_issues_count"],
            "language": r.get("language") or "Unknown",
            "topics": ", ".join(r.get("topics", [])),
            "license": r.get("license", {}).get("spdx_id", "None") if r.get("license") else "None",
            "created_at": r["created_at"],
            "updated_at": r["updated_at"],
            "url": r["html_url"],
        })
    return pd.DataFrame(rows)
