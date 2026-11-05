"""Shared Streamlit controls, avoiding duplicate page logic."""
from __future__ import annotations
import streamlit as st
import pandas as pd
from src.data_loader import load_default_dataset, load_csv, DatasetValidationError
from src.preprocessing import clean_job_data
from src.ui import inject_styles, empty_panel

@st.cache_data(show_spinner="Preparing job-posting data...")
def default_cleaned_data() -> pd.DataFrame:
    return clean_job_data(load_default_dataset()).data

def get_data() -> tuple[pd.DataFrame, str]:
    st.sidebar.markdown('<div class="js-filter-title">Data source</div>', unsafe_allow_html=True)
    upload = st.sidebar.file_uploader("Upload your CSV", type="csv", help="The file is processed only in this browser session.")
    if upload is None: return default_cleaned_data().copy(), "Fliar BI 2026 sample"
    try: return clean_job_data(load_csv(upload)).data, upload.name
    except DatasetValidationError as exc:
        st.sidebar.error(str(exc)); return pd.DataFrame(), upload.name

def apply_filters(data: pd.DataFrame) -> pd.DataFrame:
    if data.empty: return data
    st.sidebar.markdown('<div class="js-filter-title">Refine analysis</div>', unsafe_allow_html=True)
    result = data.copy()
    country_values = sorted(result["country_clean"].dropna().unique())
    default_country = ["IN"] if "IN" in country_values else country_values
    countries = st.sidebar.multiselect("Country", country_values, default=default_country)
    if countries: result = result[result["country_clean"].isin(countries)]
    for label, col in [("City", "city_clean"), ("State / region", "region"), ("Job role", "role_clean")]:
        values = sorted(result[col].dropna().unique())
        selected = st.sidebar.multiselect(label, values)
        if selected: result = result[result[col].isin(selected)]
    skill = st.sidebar.text_input("Skill contains")
    if skill: result = result[result["skills_list"].map(lambda x: skill.lower() in x)]
    availability = st.sidebar.selectbox("Salary availability", ["All", "Disclosed", "Not disclosed"])
    if availability == "Disclosed": result = result[result["salary_annual_usd"].notna() | result["salary_lpa"].notna()]
    if availability == "Not disclosed": result = result[result["salary_annual_usd"].isna() & result["salary_lpa"].isna()]
    max_exp = result["experience_years"].dropna().max()
    if pd.notna(max_exp):
        selected_exp = st.sidebar.slider("Maximum stated experience (years)", 0.0, float(max_exp), float(max_exp), 0.5)
        result = result[result["experience_years"].isna() | (result["experience_years"] <= selected_exp)]
    return result

def page_data() -> tuple[pd.DataFrame, str]:
    inject_styles()
    st.sidebar.markdown("""<div class="js-brand"><div class="js-brand-mark">J</div><div><div class="js-brand-name">JobScope India</div><small>Career market intelligence</small></div></div>""", unsafe_allow_html=True)
    st.sidebar.caption("Filters update this page. Missing values remain missing; they are never converted to zero.")
    data, label = get_data()
    return apply_filters(data), label

def empty_state(data: pd.DataFrame) -> bool:
    if data.empty:
        empty_panel()
        return True
    return False
