"""Transparent cleaning for job-posting datasets; raw data is never changed."""
from __future__ import annotations

from dataclasses import dataclass
import re
import numpy as np
import pandas as pd

TEXT_COLUMNS = ["posting_id", "title", "company", "role", "seniority", "category", "city", "region", "country", "remote", "education", "skills", "employment_type"]
SKILL_ALIASES = {
    "py": "python", "python3": "python", "ms excel": "excel", "microsoft excel": "excel",
    "structured query language": "sql", "postgres": "postgresql", "postgre sql": "postgresql",
    "amazon web services": "aws", "google cloud platform": "gcp", "power bi": "power bi",
    "machine learning": "machine learning", "ml": "machine learning", "js": "javascript",
    "node": "node.js", "nodejs": "node.js", "reactjs": "react", "c sharp": "c#",
}

@dataclass
class CleaningResult:
    data: pd.DataFrame
    audit: pd.DataFrame

def _clean_text(value: object) -> object:
    if pd.isna(value): return pd.NA
    value = re.sub(r"\s+", " ", str(value)).strip()
    return value if value else pd.NA

def standardize_skill(skill: str) -> str:
    cleaned = re.sub(r"\s+", " ", skill.strip().lower())
    return SKILL_ALIASES.get(cleaned, cleaned)

def extract_skills(value: object) -> list[str]:
    """Split only a structured skills field; description text is intentionally not mined."""
    if pd.isna(value) or not str(value).strip(): return []
    parts = re.split(r"\s*[,;|]\s*", str(value))
    return list(dict.fromkeys(standardize_skill(p) for p in parts if p.strip()))

def _parse_experience(value: object) -> float:
    if pd.isna(value) or str(value).strip() == "": return np.nan
    found = re.search(r"(\d+(?:\.\d+)?)", str(value))
    if not found: return np.nan
    number = float(found.group(1))
    return number if 0 <= number <= 50 else np.nan

def _parse_salary_text(value: object) -> tuple[float, float, str]:
    """Return annual USD, INR LPA, and currency only when units are explicit."""
    if pd.isna(value): return np.nan, np.nan, "unknown"
    text = str(value).lower().replace(",", "")
    nums = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", text)]
    if not nums: return np.nan, np.nan, "unknown"
    value = sum(nums[:2]) / min(len(nums), 2)
    if "lpa" in text or "lakh" in text or "₹" in text or "inr" in text:
        if "lakh" in text and "lpa" not in text: value /= 100000
        elif value >= 100000: value /= 100000
        return np.nan, value, "INR"
    if "$" in text or "usd" in text:
        if "k" in text: value *= 1000
        return value if "month" not in text else value * 12, np.nan, "USD"
    return np.nan, np.nan, "unknown"

def clean_job_data(raw: pd.DataFrame) -> CleaningResult:
    """Clean a copy, retaining missing values and recording every removal decision."""
    df = raw.copy()
    audit: list[dict] = []
    for col in TEXT_COLUMNS:
        if col in df: df[col] = df[col].map(_clean_text)
    if "title" not in df: df["title"] = pd.NA
    df["title_clean"] = df["title"].astype("string").str.replace(r"\s+", " ", regex=True).str.strip()
    before = len(df)
    df = df[df["title_clean"].notna()].copy()
    audit.append({"action": "removed invalid records", "rows": before-len(df), "reason": "missing job title"})
    duplicate_subset = ["posting_id"] if "posting_id" in df and df["posting_id"].notna().any() else None
    before = len(df)
    df = df.drop_duplicates(subset=duplicate_subset, keep="first")
    audit.append({"action": "removed duplicates", "rows": before-len(df), "reason": "duplicate posting ID or full row"})
    if "experience_years" in df:
        df["experience_years"] = df["experience_years"].map(_parse_experience)
    else: df["experience_years"] = np.nan
    if "skills" not in df: df["skills"] = pd.NA
    df["skills_list"] = df["skills"].map(extract_skills)
    for col in ["city", "region", "country", "role", "category", "seniority", "remote", "employment_type"]:
        if col not in df: df[col] = pd.NA
    df["city_clean"] = df["city"].astype("string").str.strip().str.title()
    df["role_clean"] = df["role"].astype("string").str.strip().str.lower()
    df["country_clean"] = df["country"].astype("string").str.strip().replace({"india": "IN", "India": "IN"})
    source_usd = pd.to_numeric(df.get("salary_annual_usd", pd.Series(np.nan, index=df.index)), errors="coerce")
    df["salary_annual_usd"] = source_usd.where((source_usd > 0) & (source_usd <= 10_000_000))
    parsed = df.get("salary_text", pd.Series(pd.NA, index=df.index)).map(_parse_salary_text)
    parsed_usd = parsed.map(lambda x: x[0]); parsed_lpa = parsed.map(lambda x: x[1]); parsed_currency = parsed.map(lambda x: x[2])
    df["salary_annual_usd"] = df["salary_annual_usd"].fillna(parsed_usd)
    df["salary_lpa"] = parsed_lpa
    df["salary_currency"] = np.where(df["salary_annual_usd"].notna(), "USD", parsed_currency)
    df["salary_outlier_flag"] = df["salary_annual_usd"].notna() & ((df["salary_annual_usd"] < 1000) | (df["salary_annual_usd"] > 1_000_000))
    audit.append({"action": "flagged salary outliers", "rows": int(df["salary_outlier_flag"].sum()), "reason": "annual USD < 1,000 or > 1,000,000; retained for transparency"})
    audit.append({"action": "retained missing salaries", "rows": int(df["salary_annual_usd"].isna().sum()), "reason": "missing pay is not zero"})
    return CleaningResult(df.reset_index(drop=True), pd.DataFrame(audit))
