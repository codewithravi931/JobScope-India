"""Location-focused analysis helpers."""
from __future__ import annotations
import pandas as pd

def location_counts(data: pd.DataFrame, field: str = "city_clean", limit: int = 20) -> pd.DataFrame:
    return (data[field].dropna().value_counts().head(limit).rename_axis(field).reset_index(name="postings")) if field in data else pd.DataFrame()

def roles_by_city(data: pd.DataFrame, limit: int = 30) -> pd.DataFrame:
    cols = ["city_clean", "role_clean"]
    return (data.dropna(subset=cols).groupby(cols).size().reset_index(name="postings")
            .sort_values("postings", ascending=False).head(limit))
