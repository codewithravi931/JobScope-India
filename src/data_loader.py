"""Safe CSV loading and schema helpers."""
from __future__ import annotations

from pathlib import Path
from typing import IO, Union
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "job_postings_2026_sample.csv"

ALIASES = {
    "job_title": "title", "position": "title", "job_role": "role",
    "location": "city", "state": "region", "skills_required": "skills",
    "skill": "skills", "experience": "experience_years", "experience_required": "experience_years",
    "salary": "salary_text", "salary_range": "salary_text", "employment_type": "employment_type",
    "date": "posted_date", "posting_date": "posted_date", "posted_on": "posted_date",
}

class DatasetValidationError(ValueError):
    """Raised when an uploaded CSV cannot support job-market analysis."""

def standardize_column_name(name: str) -> str:
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower())).strip("_")

def load_csv(source: Union[str, Path, IO[bytes]]) -> pd.DataFrame:
    """Load a non-empty CSV and normalise its headers without changing its values."""
    try:
        data = pd.read_csv(source)
    except pd.errors.EmptyDataError as exc:
        raise DatasetValidationError("The CSV file is empty.") from exc
    except UnicodeDecodeError as exc:
        raise DatasetValidationError("The file must be UTF-8 encoded CSV.") from exc
    if data.empty:
        raise DatasetValidationError("The CSV has headers but no data rows.")
    data.columns = [standardize_column_name(c) for c in data.columns]
    data = data.rename(columns={c: ALIASES.get(c, c) for c in data.columns})
    if not {"title", "skills", "city", "role"}.intersection(data.columns):
        raise DatasetValidationError(
            "CSV needs at least one recognised analysis column: title, role, skills, or city."
        )
    return data

def load_default_dataset() -> pd.DataFrame:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Default dataset is missing: {RAW_DATA_PATH}. See README.md for download instructions."
        )
    return load_csv(RAW_DATA_PATH)

def dataset_profile(data: pd.DataFrame) -> dict:
    return {
        "rows": len(data), "columns": len(data.columns),
        "missing": data.isna().sum().sort_values(ascending=False),
        "duplicates": int(data.duplicated().sum()),
        "column_names": list(data.columns),
    }
