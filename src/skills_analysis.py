"""Skills-demand calculations based solely on the structured skills field."""
from __future__ import annotations
import pandas as pd

def skill_frequency(data: pd.DataFrame, limit: int = 20) -> pd.DataFrame:
    skills = data.get("skills_list", pd.Series(dtype=object)).explode().dropna()
    result = skills.value_counts().head(limit).rename_axis("skill").reset_index(name="postings")
    result["posting_share_pct"] = (result["postings"] / len(data) * 100).round(1) if len(data) else 0.0
    return result

def skills_by_role(data: pd.DataFrame, role: str | None = None, limit: int = 12) -> pd.DataFrame:
    df = data
    if role: df = df[df["role_clean"] == role]
    skills = df[["role_clean", "skills_list"]].explode("skills_list").dropna(subset=["skills_list"])
    return (skills.groupby(["role_clean", "skills_list"]).size().reset_index(name="postings")
            .sort_values("postings", ascending=False).head(limit))

def skill_combinations(data: pd.DataFrame, limit: int = 15) -> pd.DataFrame:
    from itertools import combinations
    counts: dict[str, int] = {}
    for values in data.get("skills_list", []):
        for pair in combinations(sorted(set(values)), 2):
            label = " + ".join(pair); counts[label] = counts.get(label, 0) + 1
    return pd.DataFrame(sorted(counts.items(), key=lambda x: x[1], reverse=True)[:limit], columns=["combination", "postings"])
