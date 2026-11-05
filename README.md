# Job Market Skills and Salary Analysis — DA-021

## JobScope India

A reproducible Python and Streamlit project for exploring Indian job-posting patterns: job roles, locations, structured skills, stated experience and salary disclosure. It is designed for a college data-analytics evaluation and intentionally prioritises transparent handling of missing data over impressive-looking but unsupported claims.

## Dataset

Default source: Fliar BI, *Job Postings 2026: India and United States*, [Zenodo DOI 10.5281/zenodo.23432224](https://doi.org/10.5281/zenodo.23432224), published 2026-10-17, licence **CC BY-NC 4.0**. The downloaded `job_postings_2026_sample.csv` is a 100,009-row, 6% sample described by the source as deduplicated public postings collected January–June 2026. It contains individual postings, not aggregates, with fields such as `title`, `role`, `city`, `country`, `skills`, `experience_years`, and `salary_annual_usd`.

The default UI selects India. Its source salary is annual USD; it is not relabelled as INR/LPA. If the raw dataset is absent, download `job_postings_2026_sample.csv` from the Zenodo record and place it at `data/raw/job_postings_2026_sample.csv`.

## Technologies

Python, Pandas, NumPy, Matplotlib, Plotly, Streamlit, Jupyter Notebook, and pytest.

## Setup and use

```bash
cd JobScope-India
python3 -m pip install --user --break-system-packages -r requirements.txt
python3 -m pytest -q
python3 -m streamlit run app.py
```

To open the notebook:

```bash
python3 -m jupyterlab notebooks/Job_Market_Analysis.ipynb
```

The dashboard accepts a CSV upload, validates it, applies the same cleaning pipeline in memory, and lets users export the filtered cleaned data.

## Interface design and assets

The dashboard uses a project-owned dark navy interface with cyan/blue chart accents, responsive layouts, accessible reduced-motion behaviour, and consistent filtered-data messaging. The overview visual at `assets/career-analytics-hero.svg` is an original project SVG created for JobScope India; it uses no third-party image or stock-photo asset and needs no additional licence or dependency.

## Structure

```text
JobScope-India/
├── app.py                 # Overview and data explorer
├── pages/                 # Streamlit analysis pages
├── src/                   # Loader, cleaning, analysis and chart functions
├── data/raw/              # Original public source file (unchanged)
├── data/processed/        # Generated cleaned outputs (git-ignored)
├── notebooks/             # Reproducible academic notebook
├── reports/               # Method, findings policy and limitations
└── tests/                 # Automated checks
```

## Presentation notes

Explain that raw data is never overwritten, missing salaries are not set to zero, skills are only counted from the supplied structured field, and any salary result is shown in its known unit. These choices make the conclusions more honest and defensible in a viva.

See `reports/methodology.md` for all rules and `reports/limitations.md` before presenting conclusions.
