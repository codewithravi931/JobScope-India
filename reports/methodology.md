# Methodology

## Dataset and scope

The default raw file is the Fliar BI *Job Postings 2026: India and United States* sample, Zenodo DOI `10.5281/zenodo.23432224`, published 17 October 2026 under CC BY-NC 4.0. It contains 100,009 deduplicated public-posting records sampled from a January–June 2026 collection. The dashboard selects India (`country = IN`) by default; it does not claim the international source sample represents all Indian vacancies.

## Processing decisions

- The original CSV remains in `data/raw/`; cleaning runs on a copy.
- Headers are standardised; blank text becomes missing data.
- Records without a job title are removed. Duplicate posting IDs are removed, and every removal is listed in the cleaning audit.
- Skills are extracted only from the structured `skills` field. Common aliases such as `Py` → `python` and `MS Excel` → `excel` are standardised.
- Missing salary is preserved as missing, never as zero. The source contains `salary_annual_usd`, so source salary analysis is labelled **Annual USD**. The system supports explicit INR/LPA upload values but does not convert currencies without a stated, documented exchange-rate method.
- Salary values below USD 1,000 or above USD 1,000,000 are retained but flagged for review; the dashboard does not silently delete them.
- Group salary comparisons require at least three disclosed records.

## Reproducibility

Run the notebook top-to-bottom or run the Streamlit app. Both call the same `src/` functions and therefore use the same cleaning rules.
