import json
from pathlib import Path
import requests

URL = "https://remoteok.com/api"
OUTPUT_PATH = Path("data/raw/jobs_raw.json")
# HEADERS = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
# }


def fetch_live_jobs():
    print("Fetching live tech job postings...")

    try:
        response = requests.get(URL, timeout=10)

        if response.status_code != 200:
            print(f"Error: Received HTTP status code {response.status_code}")
            return

        data = response.json()

        jobs = data[1:] if isinstance(data, list) and len(data) > 1 else data
        OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)

        print(f"Success: Saved {len(jobs)} job records to '{OUTPUT_PATH}'.")

    except requests.exceptions.RequestException as e:
        print(f"Network error encountered: {e}")


if __name__ == "__main__":
    fetch_live_jobs()