"""Honest, unit-specific salary analysis."""
import streamlit as st

from src.dashboard import empty_state, page_data
from src.salary_analysis import salary_by_group, salary_summary, salary_units
from src.ui import metric_card, page_header, section_title
from src.visualizations import bar, histogram

st.set_page_config(page_title="Salary Analysis | JobScope India", page_icon="J", layout="wide")
data, source = page_data()
page_header("Salary Analysis", "Read pay signals with the right caveats.", "Missing salary remains missing. USD and INR LPA are displayed separately and are never silently converted or combined.", source)

if not empty_state(data):
    overall = salary_summary(data)
    units = salary_units(data)
    section_title("Disclosure snapshot", "Coverage counts any record with a valid, explicitly identified salary value.")
    a, b, c, d = st.columns(4, gap="small")
    with a: metric_card("Disclosure rate", f"{overall['disclosure_pct']:.1f}%", "of visible postings", "₹", "purple")
    with b: metric_card("Salary records", f"{overall['disclosed']:,}", "valid disclosed values", "▤", "blue")
    with c: metric_card("Undisclosed", f"{overall['total'] - overall['disclosed']:,}", "not treated as zero", "—", "orange")
    with d: metric_card("Known units", f"{len(units):,}", "shown in separate sections", "◇", "pink")

    if not units:
        st.info("No comparable, explicitly unit-labelled salary values are available for the active selection.")
    else:
        section_title("Distribution and comparisons", "Every chart below uses a single stated unit and labels its sample size.")
        tabs = st.tabs([label for _, label in units])
        for tab, (column, label) in zip(tabs, units):
            with tab:
                summary = salary_summary(data, column)
                x, y, z = st.columns(3, gap="small")
                with x: metric_card("Sample size", f"{summary['unit_records']:,}", label, "n", "blue")
                with y: metric_card("Median", f"{summary['median']:,.2f}", label, "◐", "green")
                with z: metric_card("Range", f"{summary['minimum']:,.2f} – {summary['maximum']:,.2f}", label, "↔", "orange")
                fig = histogram(data, column, f"Disclosed salary distribution — {label}", label, "#56A9DA")
                if fig:
                    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})
                roles = salary_by_group(data, "role_clean", column=column)
                cities = salary_by_group(data, "city_clean", column=column)
                left, right = st.columns(2, gap="large")
                with left:
                    if not roles.empty:
                        st.plotly_chart(bar(roles.head(15), "role_clean", "median", f"Median pay by role — {label}", True, "#A45AAE"), width="stretch", config={"displayModeBar": False})
                    else:
                        st.caption("No role group has the minimum three disclosed records for this unit.")
                with right:
                    if not cities.empty:
                        st.plotly_chart(bar(cities.head(15), "city_clean", "median", f"Median pay by city — {label}", True, "#E66CA8"), width="stretch", config={"displayModeBar": False})
                    else:
                        st.caption("No city group has the minimum three disclosed records for this unit.")
