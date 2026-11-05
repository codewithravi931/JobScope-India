import streamlit as st
from src.dashboard import page_data, empty_state
from src.experience_analysis import entry_level_count
from src.salary_analysis import salary_summary
from src.skills_analysis import skill_frequency, skills_by_role
from src.ui import metric_card, page_header, section_title

st.set_page_config(page_title="Insights | JobScope India", page_icon="◈", layout="wide")
data, _ = page_data()
page_header("Career insights", "Evidence for your next learning decision.", "Every statement on this page is recalculated from the visible records—not generated as a generic recommendation.")
if not empty_state(data):
    top, salary = skill_frequency(data, 5), salary_summary(data)
    section_title("The signal at a glance", "Use these as starting points for research, not as guarantees about every opportunity.")
    a, b, c = st.columns(3)
    with a: metric_card("Visible postings", f"{len(data):,}", "active selection", "▤")
    with b: metric_card("Salary disclosure", f"{salary['disclosure_pct']:.1f}%", salary["unit"], "¤")
    with c: metric_card("Entry-level signal", f"{entry_level_count(data):,}", "entry, fresher, intern or ≤1 year", "↗")
    if not top.empty:
        section_title("Learning priorities by frequency", "The most often listed structured skills in the active selection.")
        st.markdown(" · ".join(f"**{row.skill.title()}** &nbsp; {row.postings:,} postings" for row in top.itertuples()))
    role_data = skills_by_role(data, limit=20)
    if not role_data.empty:
        section_title("Skills commonly listed by role", "Use this table to connect a target role to skills employers explicitly list.")
        st.dataframe(role_data.rename(columns={"role_clean": "role", "skills_list": "skill"}), hide_index=True, width="stretch")
    st.warning("Interpret these observations as a sample of public postings. Skill, salary and experience coverage is incomplete, so absence in a record does not mean absence in the market.")
