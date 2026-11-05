"""Structured-skill analysis."""
import streamlit as st

from src.dashboard import empty_state, page_data
from src.skills_analysis import skill_combinations, skill_frequency, skills_by_role
from src.ui import metric_card, page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="Skills Analysis | JobScope India", page_icon="J", layout="wide")
data, source = page_data()
page_header("Skills Analysis", "Understand which explicitly listed skills recur most often.", "Percentages use all visible postings as the denominator; a single posting can list more than one skill.", source)

if not empty_state(data):
    top = skill_frequency(data, 25)
    postings_with_skills = data["skills_list"].map(bool).sum()
    a, b, c = st.columns(3, gap="small")
    with a: metric_card("Postings with skills", f"{postings_with_skills:,}", "structured skill field present", "◇", "purple")
    with b: metric_card("Unique skills", f"{data['skills_list'].explode().dropna().nunique():,}", "normalised labels", "◈", "blue")
    with c: metric_card("Top skill", top.iloc[0]["skill"].title() if not top.empty else "—", "most frequently listed", "↑", "orange")

    if top.empty:
        st.info("No structured skills are available for this selection.")
    else:
        section_title("Most demanded skills", "Counts identify postings that explicitly list the skill. They do not guarantee employment outcomes.")
        st.plotly_chart(bar(top, "skill", "postings", "Skill frequency", True, "#A45AAE"), width="stretch", config={"displayModeBar": False})
        section_title("Skill ranking table", "Posting share is the count divided by all visible postings, including records with no supplied skills.")
        st.dataframe(top.rename(columns={"skill": "Skill", "postings": "Postings", "posting_share_pct": "Share of visible postings (%)"}), hide_index=True, width="stretch", height=330)

        section_title("Role-wise skill demand", "Select a role to see its explicitly supplied skills, then use this as a learning research starting point.")
        roles = sorted(data["role_clean"].dropna().unique())
        role = st.selectbox("Role focus", ["All roles"] + roles, key="js_skill_role")
        by_role = skills_by_role(data, None if role == "All roles" else role, 25)
        if not by_role.empty:
            st.dataframe(by_role.rename(columns={"role_clean": "Role", "skills_list": "Skill", "postings": "Postings"}), hide_index=True, width="stretch")

        combos = skill_combinations(data, 10)
        if not combos.empty:
            section_title("Frequently co-listed skills", "Pairs use only records containing at least two structured skills.")
            st.dataframe(combos.rename(columns={"combination": "Skill pair", "postings": "Postings"}), hide_index=True, width="stretch")
