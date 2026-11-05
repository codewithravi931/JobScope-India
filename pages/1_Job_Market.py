"""Job market records, roles and companies."""
import streamlit as st

from src.dashboard import empty_state, page_data
from src.location_analysis import location_counts
from src.ui import metric_card, page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="Job Market | JobScope India", page_icon="J", layout="wide")
data, source = page_data()
page_header("Job Market", "Review the job postings behind the analysis.", "Use the shared sidebar filters to narrow titles, companies, roles and locations.", source)

if not empty_state(data):
    known_companies = data["company"].dropna().nunique()
    remote_count = data["remote"].astype("string").str.lower().isin(["remote", "hybrid"]).sum()
    a, b, c = st.columns(3, gap="small")
    with a:
        metric_card("Visible postings", f"{len(data):,}", "after active filters", "▤", "purple")
    with b:
        metric_card("Named companies", f"{known_companies:,}", "records with company names", "◫", "blue")
    with c:
        metric_card("Remote or hybrid", f"{remote_count:,}", "as labelled by source", "⌁", "green")

    titles = data["title_clean"].dropna().value_counts().head(15).rename_axis("title").reset_index(name="postings")
    roles = data["role_clean"].dropna().value_counts().head(15).rename_axis("role").reset_index(name="postings")
    section_title("Role landscape", "Frequency is a count of visible postings, not a measure of all hiring demand.")
    left, right = st.columns(2, gap="large")
    with left:
        fig = bar(titles, "title", "postings", "Most common job titles", True, "#A45AAE")
        if fig: st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    with right:
        fig = bar(roles, "role", "postings", "Role families", True, "#E66CA8")
        if fig: st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    section_title("Posting directory", "Column headers support sorting. Blank cells mean the source did not provide that value.")
    search = st.text_input("Search job postings", placeholder="Search title, company, city, or role", key="js_job_market_search")
    shown = data
    if search:
        fields = [field for field in ("title_clean", "company", "city_clean", "role_clean") if field in shown]
        shown = shown[shown[fields].fillna("").astype(str).apply(lambda col: col.str.contains(search, case=False, na=False)).any(axis=1)]
    columns = [column for column in ("title_clean", "company", "role_clean", "city_clean", "region", "employment_type", "experience_years", "remote") if column in shown]
    st.dataframe(shown[columns], hide_index=True, width="stretch", height=450, column_config={"title_clean": "Job title", "role_clean": "Role", "city_clean": "City", "experience_years": "Experience (years)"})
