from pipeline.extract import fetch_trending
from pipeline.transform import transform_repos
from pipeline.load import init_db, save_snapshot, update_summary

def run(language: str = "python", since_days: int = 7):
    print(f"Fetching trending {language} repos (last {since_days} days)...")
    raw = fetch_trending(language, since_days)
    print(f"  Found {len(raw)} repos")

    df = transform_repos(raw)
    print(f"  Transformed {len(df)} rows")

    conn = init_db()
    save_snapshot(df, conn)
    update_summary(conn)
    conn.close()
    print(f"  Saved to data/trending.db")
    print("Done.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", default="python")
    parser.add_argument("--since-days", type=int, default=7)
    args = parser.parse_args()
    run(args.language, args.since_days)
