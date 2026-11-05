"""JobScope India — Job Market Overview."""
from __future__ import annotations

import streamlit as st

from src.dashboard import empty_state, page_data, posting_trend
from src.experience_analysis import experience_distribution
from src.location_analysis import location_counts
from src.salary_analysis import salary_summary
from src.skills_analysis import skill_frequency
from src.ui import metric_card, page_header, section_title
from src.visualizations import bar, donut, line

st.set_page_config(page_title="JobScope India", page_icon="J", layout="wide", initial_sidebar_state="expanded")
data, source = page_data()
page_header(
    "Job Market Overview",
    "Explore job-market patterns, in-demand skills and salary transparency.",
    "All metrics and visuals reflect the active filters and the selected dataset.",
    source,
)

if not empty_state(data):
    salary = salary_summary(data)
    section_title("Market snapshot", "A compact reading of the currently visible job postings.")
    a, b, c, d = st.columns(4, gap="small")
    with a:
        metric_card("Total job postings", f"{len(data):,}", "visible records", "▤", "purple")
    with b:
        metric_card("Unique locations", f"{data['city_clean'].nunique():,}", "cities represented", "⌖", "blue")
    with c:
        metric_card("Job roles", f"{data['role_clean'].nunique():,}", "role families", "◇", "orange")
    with d:
        metric_card("Salary disclosure", f"{salary['disclosure_pct']:.1f}%", f"{salary['disclosed']:,} records with known pay", "₹", "pink")

    trend = posting_trend(data)
    section_title("Market activity & opportunity mix", "Time trends are shown only when a valid posting date is available in the active data.")
    if not trend.empty:
        st.plotly_chart(line(trend, "posted_date_clean", "postings", "Job postings over time"), width="stretch", config={"displayModeBar": False})

    roles = data["role_clean"].dropna().value_counts().head(6).rename_axis("role").reset_index(name="postings")
    skills = skill_frequency(data, 12)
    left, right = st.columns(2, gap="large")
    with left:
        fig = bar(skills, "skill", "postings", "Top demanded skills", True, "#A45AAE")
        if fig:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        else:
            st.info("Structured skills are not available for the active selection.")
    with right:
        fig = donut(roles, "role", "postings", "Role distribution")
        if fig:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        else:
            st.info("Role information is not available for the active selection.")

    section_title("Where opportunities and experience requirements appear", "Location and experience visuals exclude only records where the relevant field is missing.")
    locations = location_counts(data, limit=12)
    experience = experience_distribution(data)
    left, right = st.columns(2, gap="large")
    with left:
        fig = bar(locations, "city_clean", "postings", "Location-wise opportunities", True, "#56A9DA")
        if fig:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        else:
            st.info("Location information is not available for the active selection.")
    with right:
        fig = bar(experience, "experience_years", "postings", "Stated experience requirements", False, "#F0AD62")
        if fig:
            st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        else:
            st.info("No numeric experience values are available for the active selection.")

    section_title("Salary analysis summary", "Disclosed salaries remain in their explicitly stated units; missing values are never treated as zero.")
    if salary["disclosed"]:
        st.info(f"{salary['disclosed']:,} of {salary['total']:,} visible postings have salary information. Detailed distributions and unit-specific comparisons are available in Salary Analysis.")
    else:
        st.info("No valid salary figures are available in the active selection. This does not imply unpaid roles.")

section_title("Data explorer", "Search the cleaned records and export exactly the filtered data you are viewing.")
if not data.empty:
    query = st.text_input("Search title, company, or city", placeholder="Try ‘analyst’, a company name, or a city", key="js_explorer_search")
    shown = data
    if query:
        search_columns = [column for column in ("title_clean", "company", "city_clean") if column in shown]
        matches = shown[search_columns].fillna("").astype(str).apply(lambda column: column.str.contains(query, case=False, na=False)).any(axis=1)
        shown = shown[matches]
    display = [column for column in ("title_clean", "company", "role_clean", "city_clean", "region", "country_clean", "experience_years", "skills", "salary_annual_usd", "salary_lpa", "remote") if column in shown]
    st.dataframe(shown[display], width="stretch", hide_index=True, height=410, column_config={"title_clean": "Job title", "role_clean": "Role", "city_clean": "City", "country_clean": "Country", "experience_years": "Experience (years)", "salary_annual_usd": "Annual USD", "salary_lpa": "Annual INR LPA"})
    st.download_button("Download filtered cleaned CSV", shown.to_csv(index=False).encode("utf-8"), "jobscope_filtered_cleaned.csv", "text/csv")
