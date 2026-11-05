"""Shared data, navigation and filtering controls for the Streamlit pages."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from src.data_loader import DatasetValidationError, load_csv, load_default_dataset
from src.preprocessing import clean_job_data
from src.ui import empty_panel, inject_styles

FILTER_KEYS = ("js_countries", "js_cities", "js_regions", "js_roles", "js_skill", "js_salary", "js_experience")


@st.cache_data(show_spinner="Preparing job-posting data...")
def default_cleaned_data() -> pd.DataFrame:
    return clean_job_data(load_default_dataset()).data


def _sidebar_shell() -> None:
    st.sidebar.markdown("""<div class="js-brand"><div class="js-brand-mark">J</div><div><div class="js-brand-name">JobScope India</div><small>Career Market Intelligence</small></div></div>""", unsafe_allow_html=True)
    st.sidebar.markdown('<div class="js-nav-label">Navigation</div>', unsafe_allow_html=True)
    st.sidebar.page_link("app.py", label="Dashboard", icon="🏠")
    st.sidebar.page_link("pages/1_Job_Market.py", label="Job Market", icon="💼")
    st.sidebar.page_link("pages/2_Skills_Analysis.py", label="Skills Analysis", icon="🧠")
    st.sidebar.page_link("pages/3_Salary_Analysis.py", label="Salary Analysis", icon="💰")
    st.sidebar.page_link("pages/4_Location_Analysis.py", label="Location Analysis", icon="📍")
    st.sidebar.page_link("pages/5_Career_Insights.py", label="Career Insights", icon="✨")


def get_data() -> tuple[pd.DataFrame, str]:
    st.sidebar.markdown('<div class="js-filter-title">Data tools</div>', unsafe_allow_html=True)
    upload = st.sidebar.file_uploader("Upload dataset", type="csv", key="js_upload", help="CSV files are processed only for this browser session.")
    with st.sidebar.expander("About project"):
        st.caption("DA-021 · Job Market Skills and Salary Analysis\n\nInvertis University · B.Tech CSE")
    if upload is None:
        return default_cleaned_data().copy(), "Fliar BI 2026 sample"
    try:
        return clean_job_data(load_csv(upload)).data, upload.name
    except DatasetValidationError as exc:
        st.sidebar.error(str(exc))
        return pd.DataFrame(), upload.name


def _reset_filters() -> None:
    for key in FILTER_KEYS:
        st.session_state.pop(key, None)


def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty:
        return data
    st.sidebar.markdown('<div class="js-filter-title">Refine analysis</div>', unsafe_allow_html=True)
    if st.sidebar.button("Reset filters", use_container_width=True, key="js_reset_filters"):
        _reset_filters()
        st.rerun()

    result = data.copy()
    country_values = sorted(result["country_clean"].dropna().unique())
    default_country = ["IN"] if "IN" in country_values else country_values
    countries = st.sidebar.multiselect("Country", country_values, default=default_country, key="js_countries")
    if countries:
        result = result[result["country_clean"].isin(countries)]

    controls = (("City", "city_clean", "js_cities"), ("State / region", "region", "js_regions"), ("Job role", "role_clean", "js_roles"))
    for label, column, key in controls:
        values = sorted(result[column].dropna().unique())
        selected = st.sidebar.multiselect(label, values, key=key)
        if selected:
            result = result[result[column].isin(selected)]

    skill = st.sidebar.text_input("Skill contains", placeholder="e.g. python", key="js_skill")
    if skill:
        result = result[result["skills_list"].map(lambda values: skill.lower().strip() in values)]

    availability = st.sidebar.selectbox("Salary availability", ["All", "Disclosed", "Not disclosed"], key="js_salary")
    disclosed = result[[column for column in ("salary_annual_usd", "salary_lpa") if column in result]].notna().any(axis=1)
    if availability == "Disclosed":
        result = result[disclosed]
    elif availability == "Not disclosed":
        result = result[~disclosed]

    max_exp = result["experience_years"].dropna().max()
    if pd.notna(max_exp):
        chosen_exp = st.sidebar.slider("Maximum stated experience (years)", 0.0, float(max_exp), float(max_exp), .5, key="js_experience")
        result = result[result["experience_years"].isna() | (result["experience_years"] <= chosen_exp)]
    return result


def page_data() -> tuple[pd.DataFrame, str]:
    inject_styles()
    _sidebar_shell()
    data, label = get_data()
    return apply_filters(data), label


def empty_state(data: pd.DataFrame) -> bool:
    if data.empty:
        empty_panel()
        return True
    return False


def posting_trend(data: pd.DataFrame) -> pd.DataFrame:
    """Daily count for an actual source date field; empty when dates are unavailable."""
    if "posted_date_clean" not in data:
        return pd.DataFrame(columns=["posted_date_clean", "postings"])
    dates = data["posted_date_clean"].dropna()
    return dates.value_counts().sort_index().rename_axis("posted_date_clean").reset_index(name="postings")
