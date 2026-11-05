"""Evidence-led career observations derived from the selected data."""
import streamlit as st

from src.dashboard import empty_state, page_data
from src.experience_analysis import entry_level_count
from src.location_analysis import location_counts
from src.salary_analysis import salary_summary
from src.skills_analysis import skill_frequency, skills_by_role
from src.ui import insight, metric_card, page_header, section_title

st.set_page_config(page_title="Career Insights | JobScope India", page_icon="J", layout="wide")
data, source = page_data()
page_header("Career Insights", "Evidence for your next learning decision.", "Actual observations, interpretation and learning suggestions are separated so the dashboard does not over-promise.", source)

if not empty_state(data):
    top_skills = skill_frequency(data, 5)
    locations = location_counts(data, limit=1)
    salary = salary_summary(data)
    entry = entry_level_count(data)
    a, b, c = st.columns(3, gap="small")
    with a: metric_card("Visible postings", f"{len(data):,}", "active selection", "▤", "purple")
    with b: metric_card("Entry-level signal", f"{entry:,}", "entry, fresher, intern or ≤1 year", "↑", "blue")
    with c: metric_card("Salary disclosure", f"{salary['disclosure_pct']:.1f}%", "coverage limitation", "₹", "orange")

    section_title("1. Actual observations", "These statements are direct calculations from the current filtered dataset.")
    if not top_skills.empty:
        skill_text = ", ".join(f"{row.skill.title()} ({row.postings:,})" for row in top_skills.itertuples())
        insight(f"The five most frequently listed structured skills are {skill_text}.", "Data observation")
    if not locations.empty:
        insight(f"{locations.iloc[0]['city_clean']} has the highest posting count in the visible records ({locations.iloc[0]['postings']:,}).", "Data observation")
    insight(f"Salary information is explicitly available for {salary['disclosed']:,} of {salary['total']:,} visible postings ({salary['disclosure_pct']:.1f}%).", "Data observation")

    section_title("2. Interpretation", "These readings give context; they are not predictions or guarantees.")
    if not top_skills.empty:
        insight(f"Repeated appearance of {top_skills.iloc[0]['skill'].title()} suggests it is a useful skill to investigate alongside the requirements of your target role.", "Interpretation")
    insight("Low salary disclosure means salary comparisons should be treated as partial signals rather than a complete market benchmark.", "Interpretation")

    section_title("3. Learning suggestions", "Use the observed skills to prioritise learning; always inspect current role descriptions before committing time or money.")
    if not top_skills.empty:
        insight("Start with the most frequently listed skill that also appears in the roles you are targeting. Build a small demonstrable project, then check the Job Market page for relevant employers and locations.", "Suggested next step")
    role_data = skills_by_role(data, limit=20)
    if not role_data.empty:
        section_title("Skills commonly listed by role", "A direct link between observed role labels and their structured skills.")
        st.dataframe(role_data.rename(columns={"role_clean": "Role", "skills_list": "Skill", "postings": "Postings"}), hide_index=True, width="stretch")
