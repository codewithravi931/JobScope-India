"""Salary metrics that keep currencies and undisclosed salaries separate."""
from __future__ import annotations
import pandas as pd


SALARY_UNITS = {
    "salary_annual_usd": "Annual USD",
    "salary_lpa": "Annual INR LPA",
}


def salary_units(data: pd.DataFrame) -> list[tuple[str, str]]:
    """Return only salary units that are explicitly present in the filtered data."""
    return [(column, label) for column, label in SALARY_UNITS.items()
            if column in data and data[column].notna().any()]

def salary_column(data: pd.DataFrame, column: str | None = None) -> tuple[str | None, str]:
    if column in SALARY_UNITS and column in data and data[column].notna().any():
        return column, SALARY_UNITS[column]
    units = salary_units(data)
    if units:
        return units[0]
    return None, "No comparable salary data"

def salary_summary(data: pd.DataFrame, column: str | None = None) -> dict:
    col, label = salary_column(data, column); total = len(data)
    values = data[col].dropna() if col else pd.Series(dtype=float)
    disclosed_any = data[[c for c in SALARY_UNITS if c in data]].notna().any(axis=1).sum() if total else 0
    return {"unit": label, "total": total, "disclosed": int(disclosed_any), "unit_records": len(values),
            "disclosure_pct": (disclosed_any/total*100) if total else 0,
            "missing_pct": (1-disclosed_any/total)*100 if total else 0,
            "minimum": values.min() if len(values) else None, "maximum": values.max() if len(values) else None,
            "median": values.median() if len(values) else None, "mean": values.mean() if len(values) else None}

def salary_by_group(data: pd.DataFrame, group: str, minimum_n: int = 3, column: str | None = None) -> pd.DataFrame:
    col, label = salary_column(data, column)
    if not col or group not in data: return pd.DataFrame(columns=[group, "count", "median", "mean", "unit"])
    result = (data.dropna(subset=[col, group]).groupby(group)[col].agg(count="count", median="median", mean="mean").reset_index())
    result = result[result["count"] >= minimum_n].sort_values("median", ascending=False)
    result["unit"] = label
    return result
