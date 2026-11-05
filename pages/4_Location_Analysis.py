import streamlit as st
from src.dashboard import page_data, empty_state
from src.location_analysis import location_counts, roles_by_city
from src.ui import page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="Location | JobScope India", page_icon="◈", layout="wide")
data, _ = page_data()
page_header("Location signals", "See how roles are distributed across cities.", "Use the sidebar to narrow the view by city, state or role. Missing location values are excluded only from location-specific charts.")
if not empty_state(data):
    section_title("City-wise demand", "A clearer starting point for comparing the most represented locations.")
    st.plotly_chart(bar(location_counts(data, limit=25), "city_clean", "postings", "Postings by city", True), width="stretch", config={"displayModeBar": False})
    section_title("Role mix by city", "The table shows the most common observed city and role pairings.")
    pairs = roles_by_city(data, 30)
    if pairs.empty: st.info("City and role pairings are not available for this selection.")
    else: st.dataframe(pairs.rename(columns={"city_clean": "city", "role_clean": "role"}), hide_index=True, width="stretch")
