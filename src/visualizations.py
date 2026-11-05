"""Plotly charts aligned with the JobScope India interface system."""
from __future__ import annotations

import pandas as pd
import plotly.express as px

COLORS = ["#A45AAE", "#E66CA8", "#56A9DA", "#43BFD0", "#F0AD62", "#65BE91"]
TEXT = "#26334A"
MUTED = "#748096"
GRID = "#E9E6ED"


def _finish(fig, title: str, height: int = 350):
    fig.update_layout(
        template="plotly_white",
        title=dict(text=title, font=dict(size=15, color=TEXT), x=0.01, y=.97),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, ui-sans-serif, system-ui, sans-serif", color=MUTED, size=12),
        margin=dict(l=14, r=18, t=54, b=28),
        showlegend=False,
        height=height,
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor=GRID, font_color=TEXT),
    )
    fig.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, title=None, tickfont=dict(color=MUTED))
    fig.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, title=None, tickfont=dict(color=MUTED))
    return fig


def bar(data: pd.DataFrame, x: str, y: str, title: str, horizontal: bool = False, color: str | None = None):
    if data.empty or x not in data or y not in data:
        return None
    fig = px.bar(
        data, x=y if horizontal else x, y=x if horizontal else y,
        orientation="h" if horizontal else "v", color_discrete_sequence=[color or COLORS[0]],
    )
    if horizontal:
        fig.update_yaxes(categoryorder="total ascending")
        fig.update_traces(hovertemplate="%{y}: %{x:,}<extra></extra>")
    else:
        fig.update_traces(hovertemplate="%{x}: %{y:,}<extra></extra>")
    fig.update_traces(marker_line_width=0)
    return _finish(fig, title)


def histogram(data: pd.DataFrame, column: str, title: str, label: str, color: str | None = None):
    if data.empty or column not in data or data[column].dropna().empty:
        return None
    fig = px.histogram(data.dropna(subset=[column]), x=column, nbins=25,
                       labels={column: label}, color_discrete_sequence=[color or COLORS[2]])
    fig.update_traces(marker_line_width=0, hovertemplate=f"{label}: %{{x:,.2f}}<br>Postings: %{{y:,}}<extra></extra>")
    return _finish(fig, title)


def donut(data: pd.DataFrame, names: str, values: str, title: str):
    if data.empty or names not in data or values not in data:
        return None
    fig = px.pie(data, names=names, values=values, hole=.62, color_discrete_sequence=COLORS)
    fig.update_traces(textinfo="percent", textfont_color=TEXT, hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>")
    return _finish(fig, title, height=330)


def line(data: pd.DataFrame, x: str, y: str, title: str):
    if data.empty or x not in data or y not in data:
        return None
    fig = px.line(data, x=x, y=y, markers=True, color_discrete_sequence=[COLORS[2]])
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6), hovertemplate="%{x|%d %b %Y}: %{y:,}<extra></extra>")
    return _finish(fig, title)
