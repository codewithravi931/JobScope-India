import pandas as pd
from src.preprocessing import clean_job_data, extract_skills
from src.salary_analysis import salary_summary

def test_duplicates_missing_salary_and_skills_are_handled():
    raw=pd.DataFrame({"posting_id":["a","a","b"],"title":[" Data Analyst "," Data Analyst ","Engineer"],"skills":["Py; SQL",None,"Excel"],"salary_annual_usd":[None,None,"not-a-number"],"experience_years":["2 years","2 years","99 years"]})
    result=clean_job_data(raw)
    assert len(result.data)==2
    assert result.data.loc[0,"skills_list"]==["python","sql"]
    assert result.data["salary_annual_usd"].isna().all()
    assert result.data.loc[1,"experience_years"] != result.data.loc[1,"experience_years"]
    assert result.audit["rows"].sum() >= 1

def test_explicit_inr_lpa_is_not_mixed_with_usd():
    result=clean_job_data(pd.DataFrame({"title":["Analyst"],"salary_text":["₹ 6 LPA"]}))
    assert result.data.loc[0,"salary_lpa"] == 6
    assert result.data.loc[0,"salary_annual_usd"] != result.data.loc[0,"salary_annual_usd"]

def test_existing_lpa_and_posting_date_are_preserved():
    result=clean_job_data(pd.DataFrame({"title":["Analyst"],"salary_lpa":[8],"posted_date":["2026-01-01"]}))
    assert result.data.loc[0,"salary_lpa"] == 8
    assert result.data.loc[0,"salary_currency"] == "INR"
    assert str(result.data.loc[0,"posted_date_clean"].date()) == "2026-01-01"

def test_empty_salary_summary_is_safe():
    result=clean_job_data(pd.DataFrame({"title":["Analyst"]}))
    assert salary_summary(result.data)["disclosure_pct"] == 0

def test_skill_extraction_does_not_infer_from_unrelated_fields():
    assert extract_skills(None) == []
