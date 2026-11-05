"""JobScope India – overview dashboard and data explorer."""
from __future__ import annotations

import streamlit as st

from src.dashboard import page_data, empty_state
from src.location_analysis import location_counts
from src.salary_analysis import salary_summary
from src.skills_analysis import skill_frequency
from src.ui import metric_card, overview_hero, page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="JobScope India", page_icon="◈", layout="wide", initial_sidebar_state="expanded")
data, source = page_data()
page_header(
    "Career market intelligence",
    "The job market, made easier to read.",
    "A focused view of skills, roles, locations, experience and salary transparency. India is selected by default whenever it is available in the source.",
)
overview_hero()

if not empty_state(data):
    salary = salary_summary(data)
    section_title("Market snapshot", f"Source: {source} · Metrics reflect the active filters.")
    a, b, c, d = st.columns(4)
    with a: metric_card("Job postings", f"{len(data):,}", "matching records", "▤")
    with b: metric_card("Locations", f"{data['city_clean'].nunique():,}", "represented cities", "⌖")
    with c: metric_card("Job roles", f"{data['role_clean'].nunique():,}", "role families", "↗")
    with d: metric_card("Salary disclosed", f"{salary['disclosure_pct']:.1f}%", "known-unit coverage", "¤")

    section_title("What the market is asking for", "Structured skills and locations from the currently visible records.")
    left, right = st.columns(2, gap="large")
    with left:
        fig = bar(skill_frequency(data, 12), "skill", "postings", "Most frequently listed skills", True)
        if fig: st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        else: st.info("Skills are not available for the active selection.")
    with right:
        fig = bar(location_counts(data, limit=12), "city_clean", "postings", "Postings by city", True)
        if fig: st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

section_title("Data explorer", "Search the cleaned records, then export exactly the filtered data you are viewing.")
if not data.empty:
    query = st.text_input("Search title, company, or city", placeholder="Try ‘analyst’, a company name, or a city")
    shown = data
    if query:
        mask = shown[["title_clean", "company", "city_clean"]].fillna("").astype(str).apply(
            lambda column: column.str.contains(query, case=False, na=False)
        ).any(axis=1)
        shown = shown[mask]
    display = [column for column in ["title_clean", "company", "role_clean", "city_clean", "region", "country_clean", "experience_years", "skills", "salary_annual_usd", "salary_lpa", "remote"] if column in shown]
    st.dataframe(shown[display], width="stretch", hide_index=True, height=430)
    st.download_button("Download filtered cleaned CSV", shown.to_csv(index=False).encode("utf-8"), "jobscope_filtered_cleaned.csv", "text/csv")
