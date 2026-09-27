import json
import re

import pandas as pd
from bs4 import BeautifulSoup

from config import RAW_PATH, PROCESSED_PATH

SKILLS = [
    "python", "sql", "aws", "docker", "kubernetes", "react",
    "javascript", "typescript", "pytorch", "tensorflow",
    "pandas", "scikit-learn", "git", "linux", "rest", "c++"
]

SKILL_PATTERNS = [(skill, re.compile(rf"\b{re.escape(skill)}\b")) for skill in SKILLS]


def extract_skills(text):
    text_lower = text.lower()
    return [skill for skill, pattern in SKILL_PATTERNS if pattern.search(text_lower)]


def main():
    if not RAW_PATH.exists():
        print(f"Error: {RAW_PATH} not found. Run scraper first.")
        return

    with open(RAW_PATH, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    records = []

    for job in raw_data:
        if not isinstance(job, dict) or not job.get("position"):
            continue

        raw_desc = job.get("description", "")
        if raw_desc:
            clean_desc = BeautifulSoup(raw_desc, "html.parser").get_text(" ")
        else:
            clean_desc = ""

        tags = job.get("tags") or []
        combined_text = f"{job['position']} {' '.join(tags)} {clean_desc}"

        matched_skills = extract_skills(combined_text)

        records.append({
            "job_id": job.get("id"),
            "position": job["position"],
            "company": job.get("company", "Unknown"),
            "location": job.get("location", "Remote"),
            "salary_min": job.get("salary_min"),
            "salary_max": job.get("salary_max"),
            "skills": ",".join(matched_skills),
            "skill_count": len(matched_skills),
        })

    df = pd.DataFrame(records)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Successfully processed {len(df)} jobs -> saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
