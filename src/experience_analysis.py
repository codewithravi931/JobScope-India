"""Experience and entry-level opportunity helpers."""
from __future__ import annotations
import pandas as pd

def experience_distribution(data: pd.DataFrame) -> pd.DataFrame:
    values = data.get("experience_years", pd.Series(dtype=float)).dropna()
    return values.value_counts().sort_index().rename_axis("experience_years").reset_index(name="postings")

def entry_level_count(data: pd.DataFrame) -> int:
    seniority = data.get("seniority", pd.Series("", index=data.index)).astype("string").str.lower()
    return int(((data["experience_years"] <= 1) | seniority.isin(["entry", "fresher", "intern"])).sum())
