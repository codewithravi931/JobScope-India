"""Location-focused analysis without inferred geography."""
import streamlit as st

from src.dashboard import empty_state, page_data
from src.location_analysis import location_counts, roles_by_city
from src.ui import metric_card, page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="Location Analysis | JobScope India", page_icon="J", layout="wide")
data, source = page_data()
page_header("Location Analysis", "Compare the locations represented in the active dataset.", "Findings describe this job-posting sample, not necessarily the entire Indian job market. No map is used because reliable coordinates are not supplied.", source)

if not empty_state(data):
    locations = location_counts(data, limit=25)
    top_location = locations.iloc[0]["city_clean"] if not locations.empty else "—"
    located = data["city_clean"].notna().sum()
    a, b, c = st.columns(3, gap="small")
    with a: metric_card("Unique locations", f"{data['city_clean'].nunique():,}", "cities in visible records", "⌖", "purple")
    with b: metric_card("Top location", str(top_location), "highest posting count", "↑", "blue")
    with c: metric_card("Located records", f"{located:,}", "records with a city supplied", "▤", "green")

    section_title("Top locations", "Counts exclude only records whose city is missing.")
    fig = bar(locations, "city_clean", "postings", "Job postings by location", True, "#56A9DA")
    if fig:
        st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
    else:
        st.info("Location information is not available for the active selection.")

    section_title("Role mix by location", "These are the most common city and role combinations in the filtered records.")
    pairs = roles_by_city(data, 35)
    if pairs.empty:
        st.info("City and role pairings are not available for this selection.")
    else:
        st.dataframe(pairs.rename(columns={"city_clean": "City", "role_clean": "Role", "postings": "Postings"}), hide_index=True, width="stretch", height=400)
