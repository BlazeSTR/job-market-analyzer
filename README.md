# Job Market Analyzer

A small end-to-end pipeline that scrapes live tech job postings, extracts
skill mentions from the listings, and trains a model to predict salary
from those skills.

**Pipeline:** `scraper.py` → `clean.py` → `train.py`

## What it does

1. **`scraper.py`** — Pulls current job postings from the [RemoteOK](https://remoteok.com) public API and saves the raw JSON to `data/raw/jobs_raw.json`.
2. **`clean.py`** — Loads the raw postings, strips HTML from descriptions, and matches each listing against a fixed list of tech skills (Python, SQL, AWS, Docker, etc.) using regex. Outputs a cleaned CSV to `data/processed/jobs_cleaned.csv` with one row per job, including a comma-separated skill list and a skill count.
3. **`train.py`** — Loads the cleaned CSV, filters to jobs with a listed salary, one-hot encodes the skills, and trains a `RandomForestRegressor` to predict minimum salary from skills present. Prints MAE, R², and the top predictive features.

## Setup

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the three stages in order:

```bash
python src/scraper.py
python src/clean.py
python src/train.py
```

Each stage reads the previous stage's output; running one out of order will
print a clear error telling you which step to run first.

`config.py` holds the shared file paths so all three scripts stay in sync.

## Current limitation: sparse salary data

RemoteOK only lists a real `salary_min`/`salary_max` for a minority of
postings — in a typical scrape of ~100 jobs, only around 15–20 have a
usable salary figure. With that few labeled examples, the current model
does not generalize: in testing, R² came out negative, meaning it performed
worse than simply predicting the average salary for every job.

This is a data-availability problem, not a bug in the pipeline — the
scraping, cleaning, and feature engineering all work correctly, but there
isn't yet enough labeled data for the model to learn real patterns.

**Planned improvements:**
- Aggregate postings from multiple job boards (not just RemoteOK) to
  increase the number of salary-labeled rows.
- Add a naive baseline (predict the mean) to properly benchmark model
  performance against.
- Try simpler models (e.g. linear regression) better suited to small
  sample sizes, and revisit RandomForest once more data is available.
- Explore embedding-based skill extraction instead of fixed keyword
  matching, to capture skills not in the current hardcoded list.

## Tech stack

Python, pandas, scikit-learn, BeautifulSoup, requests
