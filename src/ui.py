"""Shared presentation components for the JobScope India Streamlit interface."""
from __future__ import annotations

from pathlib import Path
import html
import streamlit as st

ASSET_DIR = Path(__file__).resolve().parents[1] / "assets"

def inject_styles() -> None:
    """Apply the app-wide visual system without altering data or calculations."""
    st.markdown("""
    <style>
    :root { --js-bg:#09111f; --js-surface:#101c2e; --js-surface-2:#15243a; --js-border:#263a55; --js-text:#f2f6fc; --js-muted:#9dafc4; --js-cyan:#53c8e9; --js-blue:#628cff; --js-good:#75d6b3; }
    .stApp { background: radial-gradient(900px 480px at 84% -12%, rgba(60,120,190,.14), transparent 65%), var(--js-bg); color:var(--js-text); }
    .block-container { max-width:1480px; padding:1.35rem 2.25rem 3.5rem; }
    [data-testid="stHeader"] { background:rgba(9,17,31,.88); border-bottom:1px solid rgba(38,58,85,.55); }
    [data-testid="stSidebar"] { background:#0b1525; border-right:1px solid var(--js-border); }
    [data-testid="stSidebar"] > div:first-child { padding-top:.65rem; }
    [data-testid="stSidebar"] .stMarkdown p { color:var(--js-muted); }
    [data-testid="stSidebarNav"] { padding-top:1rem; }
    [data-testid="stSidebarNav"] a { border-radius:9px; color:#bbcadb; margin:.1rem .45rem; transition:background .18s ease,color .18s ease,transform .18s ease; }
    [data-testid="stSidebarNav"] a:hover, [data-testid="stSidebarNav"] a[aria-current="page"] { background:#152a43; color:#fff; transform:translateX(2px); }
    .js-brand { display:flex; align-items:center; gap:.7rem; padding:.4rem .25rem 1rem; border-bottom:1px solid var(--js-border); margin-bottom:1.15rem; }
    .js-brand-mark { display:grid; place-items:center; width:32px; height:32px; border-radius:9px; background:linear-gradient(145deg,#53c8e9,#5379e8); color:#07111f; font-weight:800; }
    .js-brand-name { color:#f8fbff; font-weight:700; letter-spacing:-.02em; font-size:1.03rem; }.js-brand small{display:block;color:var(--js-muted);font-size:.7rem;margin-top:1px}
    .js-filter-title { text-transform:uppercase; letter-spacing:.11em; font-size:.7rem; color:#7189a5; font-weight:700; margin:1.25rem 0 .25rem; }
    .js-page { animation:js-fade .45s ease both; }.js-eyebrow { color:var(--js-cyan); text-transform:uppercase; letter-spacing:.12em; font-size:.72rem; font-weight:750; margin-bottom:.35rem; }.js-page h1 { font-size:2rem; letter-spacing:-.045em; margin:0; color:var(--js-text); line-height:1.1; }.js-page p { color:var(--js-muted); max-width:760px; margin:.52rem 0 1.35rem; font-size:.96rem; }
    .js-panel { border:1px solid var(--js-border); background:linear-gradient(150deg,rgba(21,36,58,.92),rgba(14,26,43,.92)); border-radius:14px; padding:1rem 1.1rem; box-shadow:0 12px 30px rgba(0,0,0,.12); }
    .js-section-title { color:var(--js-text); font-size:1.03rem; font-weight:700; margin:1.65rem 0 .15rem; letter-spacing:-.015em; }.js-section-copy{color:var(--js-muted);font-size:.85rem;margin-bottom:.7rem}
    .js-metric { min-height:118px; border:1px solid var(--js-border); border-radius:14px; padding:1rem; background:linear-gradient(145deg,#13223a,#101c2e); animation:js-rise .45s ease both; transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease; }.js-metric:hover{transform:translateY(-3px);border-color:#3d6289;box-shadow:0 12px 24px rgba(0,0,0,.2)}.js-metric-top{display:flex;justify-content:space-between;align-items:center}.js-metric-icon{display:grid;place-items:center;width:24px;height:24px;border-radius:7px;border:1px solid #315574;background:#102c44;color:#68d0eb;font-size:.9rem;line-height:1}.js-metric-kicker{color:#9dafc4;font-size:.78rem}.js-metric-value{font-size:1.65rem;font-weight:750;letter-spacing:-.05em;color:#f7fbff;margin:.38rem 0 .2rem}.js-metric-note{color:#6fd4ee;font-size:.73rem}
    .js-hero { border:1px solid var(--js-border); border-radius:16px; background:linear-gradient(115deg,#111f35 0%,#10233a 62%,#0d1a2c 100%); overflow:hidden; padding:1.45rem; margin:.2rem 0 1.25rem; }.js-hero h2{font-size:1.65rem;letter-spacing:-.04em;margin:.45rem 0 .55rem;line-height:1.13}.js-hero p{margin:0;color:#b5c4d7;line-height:1.55}.js-badge{display:inline-flex;align-items:center;gap:.35rem;border:1px solid #315574;border-radius:999px;background:rgba(83,200,233,.08);color:#8edcf1;padding:.28rem .58rem;font-size:.72rem;font-weight:650}.js-source{color:#8297af;font-size:.75rem;margin-top:.8rem}
    .stButton>button, .stDownloadButton>button { border:1px solid #356486; background:#153451; color:#eaf8ff; border-radius:8px; font-weight:650; transition:transform .18s ease, background .18s ease, border-color .18s ease; }.stButton>button:hover,.stDownloadButton>button:hover { transform:translateY(-1px); background:#1b4668; border-color:#54c8e8; color:#fff; }
    [data-testid="stDataFrame"] { border:1px solid var(--js-border); border-radius:12px; overflow:hidden; }.stTextInput input,.stSelectbox [data-baseweb="select"]>div,.stMultiSelect [data-baseweb="select"]>div { background:#101c2e !important; border-color:#304763 !important; border-radius:8px !important; }
    [data-testid="stMetric"] { background:#13223a; border:1px solid var(--js-border); border-radius:12px; padding:.75rem; }.stAlert{border-radius:10px}.stPlotlyChart{border:1px solid var(--js-border);border-radius:14px;background:rgba(16,28,46,.65);padding:.2rem;overflow:hidden;animation:js-rise .5s ease both}
    .js-empty{border:1px dashed #3a5573;border-radius:12px;background:#101c2e;padding:1.4rem;text-align:center;color:#b8c7d8}.js-empty strong{color:#f4f8fd;display:block;margin-bottom:.35rem}
    @keyframes js-fade { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:none} } @keyframes js-rise { from{opacity:0;transform:translateY(7px)} to{opacity:1;transform:none} }
    @media (max-width: 760px) { .block-container{padding:1rem 1rem 2.5rem}.js-page h1{font-size:1.62rem}.js-hero{padding:1.1rem}.js-metric{min-height:98px;padding:.8rem}.js-metric-value{font-size:1.35rem} }
    @media (prefers-reduced-motion: reduce) { *,*::before,*::after { animation-duration:.01ms !important; animation-iteration-count:1 !important; transition-duration:.01ms !important; scroll-behavior:auto !important; } }
    </style>
    """, unsafe_allow_html=True)

def page_header(eyebrow: str, title: str, description: str) -> None:
    st.markdown(f'<section class="js-page"><div class="js-eyebrow">{html.escape(eyebrow)}</div><h1>{html.escape(title)}</h1><p>{html.escape(description)}</p></section>', unsafe_allow_html=True)

def section_title(title: str, description: str = "") -> None:
    st.markdown(f'<div class="js-section-title">{html.escape(title)}</div><div class="js-section-copy">{html.escape(description)}</div>', unsafe_allow_html=True)

def metric_card(label: str, value: str, note: str, icon: str = "◈") -> None:
    st.markdown(f'<div class="js-metric"><div class="js-metric-top"><div class="js-metric-kicker">{html.escape(label)}</div><span class="js-metric-icon" aria-hidden="true">{html.escape(icon)}</span></div><div class="js-metric-value">{html.escape(value)}</div><div class="js-metric-note">{html.escape(note)}</div></div>', unsafe_allow_html=True)

def overview_hero() -> None:
    left, right = st.columns([1.2, .8], gap="large")
    with left:
        st.markdown("""<div class="js-hero"><span class="js-badge">● Live analysis workspace</span><h2>Turn market signals into a focused career direction.</h2><p>Explore roles, skills, experience requirements and salary disclosure using transparent, filterable job-posting data.</p><div class="js-source">DA-021 · Job Market Skills and Salary Analysis</div></div>""", unsafe_allow_html=True)
    with right:
        st.image(str(ASSET_DIR / "career-analytics-hero.svg"), width="stretch")

def empty_panel() -> None:
    st.markdown('<div class="js-empty"><strong>No matching records</strong>Adjust or clear one or more filters to bring data back into view.</div>', unsafe_allow_html=True)
