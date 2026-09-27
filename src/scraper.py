import json
import requests

from config import RAW_PATH

URL = "https://remoteok.com/api"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_live_jobs():
    print("Fetching live tech job postings...")

    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            print(f"Error: Received HTTP status code {response.status_code}")
            return

        try:
            data = response.json()
        except ValueError:
            print("Error: Response was not valid JSON (site may be blocking the request).")
            return

        if not isinstance(data, list):
            print("Error: Unexpected response format from RemoteOK.")
            return

        # RemoteOK's first list item is a legal notice, not a job posting.
        jobs = [job for job in data if isinstance(job, dict) and job.get("id")]

        RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(RAW_PATH, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)

        print(f"Success: Saved {len(jobs)} job records to '{RAW_PATH}'.")

    except requests.exceptions.RequestException as e:
        print(f"Network error encountered: {e}")


if __name__ == "__main__":
    fetch_live_jobs()
