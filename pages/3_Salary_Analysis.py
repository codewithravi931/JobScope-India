import streamlit as st
from src.dashboard import page_data, empty_state
from src.salary_analysis import salary_by_group, salary_column, salary_summary
from src.ui import metric_card, page_header, section_title
from src.visualizations import bar, histogram

st.set_page_config(page_title="Salary | JobScope India", page_icon="◈", layout="wide")
data, _ = page_data()
page_header("Salary clarity", "Read salary signals with the right caveats.", "Pay comparisons use only values with a known unit. Undisclosed salary is always kept separate from zero.")
if not empty_state(data):
    summary = salary_summary(data); column, label = salary_column(data)
    section_title("Disclosure snapshot", "Salary measurements below are calculated only from disclosed values.")
    a, b, c, d = st.columns(4)
    with a: metric_card("Coverage", f"{summary['disclosure_pct']:.1f}%", "of visible postings", "¤")
    with b: metric_card("Median", f"{summary['median']:,.2f}" if summary["median"] is not None else "—", label, "◐")
    with c: metric_card("Average", f"{summary['mean']:,.2f}" if summary["mean"] is not None else "—", label, "↗")
    with d: metric_card("Known unit", label, "no speculative conversion", "i")
    if column:
        fig = histogram(data, column, "Disclosed salary distribution", label)
        if fig: st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
        role, city = salary_by_group(data, "role_clean"), salary_by_group(data, "city_clean")
        section_title("Salary comparison", "Groups need at least three disclosed records to appear.")
        left, right = st.columns(2, gap="large")
        with left:
            if not role.empty: st.plotly_chart(bar(role.head(15), "role_clean", "median", "Median pay by role", True), width="stretch", config={"displayModeBar": False})
        with right:
            if not city.empty: st.plotly_chart(bar(city.head(15), "city_clean", "median", "Median pay by city", True), width="stretch", config={"displayModeBar": False})
    else: st.info("No comparable, explicitly unit-labelled salary values are available.")
