"""Salary metrics that keep currencies and undisclosed salaries separate."""
from __future__ import annotations
import pandas as pd

def salary_column(data: pd.DataFrame) -> tuple[str | None, str]:
    if data.get("salary_annual_usd", pd.Series(dtype=float)).notna().any(): return "salary_annual_usd", "Annual USD"
    if data.get("salary_lpa", pd.Series(dtype=float)).notna().any(): return "salary_lpa", "INR LPA"
    return None, "No comparable salary data"

def salary_summary(data: pd.DataFrame) -> dict:
    col, label = salary_column(data); total = len(data)
    values = data[col].dropna() if col else pd.Series(dtype=float)
    return {"unit": label, "total": total, "disclosed": len(values),
            "disclosure_pct": (len(values)/total*100) if total else 0,
            "missing_pct": (1-len(values)/total)*100 if total else 0,
            "minimum": values.min() if len(values) else None, "maximum": values.max() if len(values) else None,
            "median": values.median() if len(values) else None, "mean": values.mean() if len(values) else None}

def salary_by_group(data: pd.DataFrame, group: str, minimum_n: int = 3) -> pd.DataFrame:
    col, label = salary_column(data)
    if not col or group not in data: return pd.DataFrame(columns=[group, "count", "median", "mean", "unit"])
    result = (data.dropna(subset=[col, group]).groupby(group)[col].agg(count="count", median="median", mean="mean").reset_index())
    result = result[result["count"] >= minimum_n].sort_values("median", ascending=False)
    result["unit"] = label
    return result
