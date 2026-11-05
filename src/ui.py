"""Shared presentation components for the JobScope India Streamlit interface."""
from __future__ import annotations

import html
import streamlit as st


def inject_styles() -> None:
    """Apply the pastel analytics visual system without changing any calculations."""
    st.markdown("""
    <style>
    :root { --js-canvas:#F8E8F1; --js-surface:#FFFFFF; --js-text:#26334A; --js-muted:#748096; --js-faint:#929BAB; --js-border:#E9E6ED; --js-purple-soft:#F3E4F5; --js-purple:#A45AAE; --js-pink:#E66CA8; --js-blue-soft:#E4F1FA; --js-blue:#56A9DA; --js-cyan:#43BFD0; --js-orange-soft:#FFF0DB; --js-orange:#F0AD62; --js-green:#65BE91; }
    .stApp { background:var(--js-canvas); color:var(--js-text); }
    .block-container { max-width:1480px; padding:1.25rem 2rem 3rem; }
    [data-testid="stHeader"] { background:rgba(248,232,241,.94); border-bottom:1px solid rgba(233,230,237,.72); }
    [data-testid="stSidebar"] { background:#FFFFFF; border-right:1px solid var(--js-border); }
    [data-testid="stSidebar"] > div:first-child { padding:1rem .72rem 2rem; }
    [data-testid="stSidebar"] [data-testid="stSidebarNav"] { display:none; }
    [data-testid="stSidebar"] .stCaption { color:var(--js-muted); line-height:1.45; }
    .js-brand { display:flex; align-items:center; gap:.72rem; padding:.28rem .3rem 1.15rem; margin-bottom:.7rem; border-bottom:1px solid var(--js-border); }
    .js-brand-mark { display:grid; place-items:center; width:34px; height:34px; border-radius:10px; background:var(--js-purple-soft); color:var(--js-purple); font-weight:800; font-size:1.05rem; }
    .js-brand-name { color:var(--js-text); font-weight:780; letter-spacing:-.03em; font-size:1.04rem; }.js-brand small{display:block;color:var(--js-muted);font-size:.7rem;margin-top:2px}
    .js-nav-label,.js-filter-title { text-transform:uppercase; letter-spacing:.12em; font-size:.66rem; color:var(--js-faint); font-weight:800; margin:1.1rem .35rem .4rem; }
    [data-testid="stSidebar"] [data-testid="stPageLink"] { margin:.07rem 0; }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a { border-radius:8px; color:var(--js-muted); padding:.52rem .58rem; font-size:.88rem; transition:background .16s ease,color .16s ease; }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover { background:#FBF4F8; color:var(--js-purple); }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] { background:var(--js-purple-soft); color:var(--js-purple); font-weight:700; }
    .js-page { background:var(--js-surface); border:1px solid var(--js-border); border-radius:14px; padding:1.05rem 1.25rem; margin:0 0 1rem; }
    .js-topline { display:flex; justify-content:space-between; gap:1rem; align-items:center; margin-bottom:.55rem; }.js-eyebrow { color:var(--js-purple); text-transform:uppercase; letter-spacing:.115em; font-size:.68rem; font-weight:800; }.js-status { color:var(--js-muted); font-size:.74rem; background:#FAFAFC; border:1px solid var(--js-border); border-radius:999px; padding:.26rem .55rem; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:45%; }
    .js-page h1 { color:var(--js-text); font-size:1.72rem; letter-spacing:-.045em; margin:0; line-height:1.14; }.js-page p { color:var(--js-muted); max-width:780px; margin:.45rem 0 0; font-size:.91rem; line-height:1.5; }
    .js-section-title { color:var(--js-text); font-size:1.02rem; font-weight:760; margin:1.55rem 0 .17rem; letter-spacing:-.018em; }.js-section-copy{color:var(--js-muted);font-size:.83rem;margin-bottom:.68rem;line-height:1.45}
    .js-metric { min-height:113px; border:1px solid var(--js-border); border-radius:12px; padding:.9rem 1rem; background:var(--js-surface); transition:transform .16s ease,border-color .16s ease; }.js-metric:hover{transform:translateY(-2px);border-color:#D9CBDD}.js-metric.purple{background:#FCF9FD;border-top:3px solid var(--js-purple)}.js-metric.pink{background:#FFF8FB;border-top:3px solid var(--js-pink)}.js-metric.blue{background:#F8FCFE;border-top:3px solid var(--js-blue)}.js-metric.orange{background:#FFFDF9;border-top:3px solid var(--js-orange)}.js-metric.green{background:#FAFDFB;border-top:3px solid var(--js-green)}
    .js-metric-top{display:flex;justify-content:space-between;align-items:center}.js-metric-icon{display:grid;place-items:center;width:26px;height:26px;border-radius:7px;background:#fff;border:1px solid var(--js-border);color:var(--js-purple);font-size:.82rem;line-height:1}.js-metric-kicker{color:var(--js-muted);font-size:.76rem;font-weight:650}.js-metric-value{font-size:1.65rem;font-weight:780;letter-spacing:-.05em;color:var(--js-text);margin:.35rem 0 .18rem}.js-metric-note{color:var(--js-faint);font-size:.72rem}
    .js-insight { background:#FFFFFF; border:1px solid var(--js-border); border-left:3px solid var(--js-purple); border-radius:10px; padding:.8rem .9rem; color:var(--js-muted); font-size:.84rem; line-height:1.5; margin:.36rem 0; }.js-insight strong { color:var(--js-text); }
    .stButton>button,.stDownloadButton>button { border:1px solid #D9C8DD; background:#FFFFFF; color:var(--js-purple); border-radius:8px; font-weight:700; font-size:.82rem; }.stButton>button:hover,.stDownloadButton>button:hover { border-color:var(--js-purple); background:var(--js-purple-soft); color:var(--js-purple); }
    .stTextInput input,.stSelectbox [data-baseweb="select"]>div,.stMultiSelect [data-baseweb="select"]>div,[data-baseweb="base-input"] { background:#FFFFFF !important; border-color:var(--js-border) !important; border-radius:8px !important; color:var(--js-text) !important; }.stTextInput input:focus,.stSelectbox [data-baseweb="select"]>div:focus-within,.stMultiSelect [data-baseweb="select"]>div:focus-within { border-color:var(--js-purple) !important; box-shadow:0 0 0 1px var(--js-purple) !important; }
    [data-testid="stDataFrame"],.stPlotlyChart { background:#FFFFFF; border:1px solid var(--js-border); border-radius:12px; overflow:hidden; }.stPlotlyChart { padding:.1rem; }.stTabs [data-baseweb="tab-list"] { gap:1.2rem; }.stTabs [data-baseweb="tab"] { color:var(--js-muted); padding:.4rem .08rem; }.stTabs [aria-selected="true"] { color:var(--js-purple) !important; border-bottom-color:var(--js-purple) !important; }.stAlert { border-radius:10px; }
    .js-empty{border:1px dashed #D8CEDA;border-radius:12px;background:#FFFFFF;padding:1.4rem;text-align:center;color:var(--js-muted)}.js-empty strong{color:var(--js-text);display:block;margin-bottom:.35rem}
    @media (max-width:760px) { .block-container{padding:.9rem .85rem 2.3rem}.js-page{padding:.9rem 1rem}.js-page h1{font-size:1.45rem}.js-status{display:none}.js-metric{min-height:98px;padding:.8rem}.js-metric-value{font-size:1.35rem} }
    @media (prefers-reduced-motion:reduce) { *,*::before,*::after { transition:none!important; } }
    </style>
    """, unsafe_allow_html=True)


def page_header(title: str, subtitle: str, description: str, source: str = "") -> None:
    status = f"Dataset: {html.escape(source)}" if source else "Filtered dataset"
    st.markdown(f'<section class="js-page"><div class="js-topline"><div class="js-eyebrow">Career &amp; labour market analytics</div><div class="js-status">{status}</div></div><h1>{html.escape(title)}</h1><p><strong>{html.escape(subtitle)}</strong> &nbsp;{html.escape(description)}</p></section>', unsafe_allow_html=True)


def section_title(title: str, description: str = "") -> None:
    st.markdown(f'<div class="js-section-title">{html.escape(title)}</div><div class="js-section-copy">{html.escape(description)}</div>', unsafe_allow_html=True)


def metric_card(label: str, value: str, note: str, icon: str = "•", tone: str = "purple") -> None:
    st.markdown(f'<div class="js-metric {html.escape(tone)}"><div class="js-metric-top"><div class="js-metric-kicker">{html.escape(label)}</div><span class="js-metric-icon" aria-hidden="true">{html.escape(icon)}</span></div><div class="js-metric-value">{html.escape(value)}</div><div class="js-metric-note">{html.escape(note)}</div></div>', unsafe_allow_html=True)


def insight(text: str, lead: str = "Observation") -> None:
    st.markdown(f'<div class="js-insight"><strong>{html.escape(lead)}.</strong> {html.escape(text)}</div>', unsafe_allow_html=True)


def empty_panel() -> None:
    st.markdown('<div class="js-empty"><strong>No matching records</strong>Adjust or reset one or more filters to bring data back into view.</div>', unsafe_allow_html=True)
