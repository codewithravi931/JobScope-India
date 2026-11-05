import streamlit as st
from src.dashboard import page_data, empty_state
from src.location_analysis import location_counts
from src.ui import page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="Job Market | JobScope India", page_icon="◈", layout="wide")
data, _ = page_data()
page_header("Market map", "Where opportunity is concentrated.", "Compare the titles, role families and cities represented by the active job-posting selection.")
if not empty_state(data):
    titles = data["title_clean"].value_counts().head(20).rename_axis("title").reset_index(name="postings")
    roles = data["role_clean"].value_counts().head(15).rename_axis("role").reset_index(name="postings")
    section_title("Role landscape", "Frequency is a count of visible postings, not a measure of total hiring demand.")
    left, right = st.columns(2, gap="large")
    with left: st.plotly_chart(bar(titles, "title", "postings", "Most common job titles", True), width="stretch", config={"displayModeBar": False})
    with right: st.plotly_chart(bar(roles, "role", "postings", "Role families", True), width="stretch", config={"displayModeBar": False})
    section_title("Geographic demand", "Cities are standardised where the source provides a location.")
    st.plotly_chart(bar(location_counts(data, limit=20), "city_clean", "postings", "Postings by city", True), width="stretch", config={"displayModeBar": False})
    if data["employment_type"].notna().any():
        types = data["employment_type"].value_counts().rename_axis("employment_type").reset_index(name="postings")
        st.plotly_chart(bar(types, "employment_type", "postings", "Employment type"), width="stretch", config={"displayModeBar": False})
    else: st.info("Employment type is not supplied by the active dataset.")
