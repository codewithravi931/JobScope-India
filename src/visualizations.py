"""Consistent accessible Plotly charts for the dashboard."""
from __future__ import annotations
import plotly.express as px
import pandas as pd

COLORS = ["#53c8e9", "#628cff", "#75d6b3", "#a78bfa", "#f5ad70"]

def _finish(fig, title: str):
    fig.update_layout(
        template="plotly_dark", title=dict(text=title, font=dict(size=16, color="#f2f6fc"), x=.02),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, ui-sans-serif, system-ui, sans-serif", color="#b8c7d8"),
        margin=dict(l=12, r=16, t=58, b=18), showlegend=False,
        transition=dict(duration=350, easing="cubic-in-out"), hoverlabel=dict(bgcolor="#14243a", bordercolor="#36536f", font_color="#f2f6fc"),
    )
    fig.update_xaxes(gridcolor="rgba(103,132,163,.16)", zerolinecolor="rgba(103,132,163,.22)", title=None)
    fig.update_yaxes(gridcolor="rgba(103,132,163,.16)", zerolinecolor="rgba(103,132,163,.22)", title=None)
    return fig

def bar(data: pd.DataFrame, x: str, y: str, title: str, horizontal: bool = False):
    if data.empty: return None
    fig = px.bar(data, x=y if horizontal else x, y=x if horizontal else y, orientation="h" if horizontal else "v", color_discrete_sequence=COLORS)
    fig.update_traces(marker_line_width=0, marker_color=COLORS[0], hovertemplate="%{y}: %{x:,}<extra></extra>" if horizontal else "%{x}: %{y:,}<extra></extra>")
    return _finish(fig, title)

def histogram(data: pd.DataFrame, column: str, title: str, label: str):
    if data.empty or column not in data or data[column].dropna().empty: return None
    fig = px.histogram(data.dropna(subset=[column]), x=column, nbins=25, labels={column: label}, color_discrete_sequence=COLORS)
    fig.update_traces(marker_line_width=0, marker_color=COLORS[1], hovertemplate=f"{label}: %{{x:,.2f}}<br>Postings: %{{y:,}}<extra></extra>")
    return _finish(fig, title)
