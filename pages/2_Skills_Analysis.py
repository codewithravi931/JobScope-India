import streamlit as st
from src.dashboard import page_data, empty_state
from src.skills_analysis import skill_combinations, skill_frequency, skills_by_role
from src.ui import page_header, section_title
from src.visualizations import bar

st.set_page_config(page_title="Skills | JobScope India", page_icon="◈", layout="wide")
data, _ = page_data()
page_header("Skills signal", "Build around the skills employers name.", "Explore only the source dataset’s structured skills field—unrelated description text is not used to infer requirements.")
if not empty_state(data):
    top = skill_frequency(data, 25)
    if top.empty:
        st.info("No structured skills are available for this selection.")
    else:
        section_title("Most listed skills", "Counts reflect the current filters and may include the same skill across multiple roles.")
        st.plotly_chart(bar(top, "skill", "postings", "Skill frequency", True), width="stretch", config={"displayModeBar": False})
        section_title("Skills by role", "Choose a role to focus the comparison.")
        roles = sorted(data["role_clean"].dropna().unique())
        role = st.selectbox("Role focus", ["All roles"] + roles)
        by_role = skills_by_role(data, None if role == "All roles" else role, 20)
        if not by_role.empty: st.dataframe(by_role.rename(columns={"role_clean": "role", "skills_list": "skill"}), hide_index=True, width="stretch")
        combos = skill_combinations(data, 10)
        if not combos.empty:
            section_title("Frequently co-listed skills", "Pairs are drawn only from records with multiple structured skills.")
            st.dataframe(combos, hide_index=True, width="stretch")
