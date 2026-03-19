import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

BG   = "#080c10"
BG2  = "#0e1419"
GRID = "rgba(255,255,255,0.04)"
TEXT = "#e8edf2"
MUTED= "#5a6a7a"
GRN  = "#00d084"
RED  = "#ff4d6d"
BLUE = "#3b9eff"
YLW  = "#f5c518"

BASE = dict(
    paper_bgcolor=BG, plot_bgcolor=BG2,
    font=dict(family="Inter, sans-serif", color=TEXT, size=12),
    margin=dict(l=10, r=10, t=36, b=10),
    hovermode="x unified",
    hoverlabel=dict(bgcolor=BG2, bordercolor=GRID, font=dict(color=TEXT)),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED, size=11)),
    xaxis=dict(gridcolor=GRID, zeroline=False, showline=False, tickfont=dict(color=MUTED, size=10)),
    yaxis=dict(gridcolor=GRID, zeroline=False, showline=False, tickfont=dict(color=MUTED, size=10)),
)


def candle(df, symbol, bb=True, ema=True):
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True,
                        row_heights=[0.55, 0.25, 0.20], vertical_spacing=0.03)

    fig.add_trace(go.Candlestick(
        x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"],
        name=symbol,
        increasing_line_color=GRN, decreasing_line_color=RED,
        increasing_fillcolor=GRN,  decreasing_fillcolor=RED,
    ), row=1, col=1)

    if bb and "BB_up" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["BB_up"], name="BB Upper",
            line=dict(color=YLW, width=1, dash="dot"), opacity=.5), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["BB_dn"], name="BB Lower",
            line=dict(color=YLW, width=1, dash="dot"), opacity=.5,
            fill="tonexty", fillcolor="rgba(245,197,24,.03)"), row=1, col=1)

    if ema and "EMA20" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], name="EMA 20",
            line=dict(color=BLUE, width=1.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["EMA50"], name="EMA 50",
            line=dict(color="#b388ff", width=1.5)), row=1, col=1)

    colors = [GRN if c >= o else RED for c, o in zip(df["Close"], df["Open"])]
    fig.add_trace(go.Bar(x=df.index, y=df["Volume"], name="Volume",
        marker_color=colors, opacity=.6), row=2, col=1)

    if "RSI" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["RSI"], name="RSI",
            line=dict(color="#ff9f43", width=1.5)), row=3, col=1)
        for level, color in [(70, RED), (30, GRN)]:
            fig.add_hline(y=level, line_dash="dot", line_color=color,
                          opacity=.4, row=3, col=1)

    layout = BASE.copy()
    layout.update(
        title=dict(text=f"<b>{symbol}</b>", font=dict(size=15, color=TEXT)),
        xaxis_rangeslider_visible=False, height=680,
        xaxis3=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED, size=10)),
        yaxis2=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED, size=10)),
        yaxis3=dict(gridcolor=GRID, zeroline=False, range=[0, 100], tickfont=dict(color=MUTED, size=10)),
    )
    fig.update_layout(**layout)
    return fig


def line(df, symbol):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df["Close"], name=symbol, mode="lines",
        line=dict(color=GRN, width=2),
        fill="tozeroy", fillcolor="rgba(0,208,132,.05)",
    ))
    layout = BASE.copy()
    layout.update(title=dict(text=f"<b>{symbol}</b> — Price", font=dict(size=15, color=TEXT)), height=380)
    fig.update_layout(**layout)
    return fig


def macd_chart(df, symbol):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        row_heights=[0.55, 0.45], vertical_spacing=0.05)
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close",
        line=dict(color=GRN, width=2)), row=1, col=1)
    if "MACD" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["MACD"], name="MACD",
            line=dict(color=BLUE, width=2)), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=df["MACD_s"], name="Signal",
            line=dict(color=YLW, width=1.5, dash="dash")), row=2, col=1)
        colors = [GRN if v >= 0 else RED for v in df["MACD_h"]]
        fig.add_trace(go.Bar(x=df.index, y=df["MACD_h"], name="Histogram",
            marker_color=colors, opacity=.7), row=2, col=1)

    layout = BASE.copy()
    layout.update(
        title=dict(text=f"<b>{symbol}</b> — MACD", font=dict(size=15, color=TEXT)),
        height=480,
        xaxis2=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED, size=10)),
        yaxis2=dict(gridcolor=GRID, zeroline=False, tickfont=dict(color=MUTED, size=10)),
    )
    fig.update_layout(**layout)
    return fig


def compare(hists: dict, mode="normalized"):
    fig = go.Figure()
    palette = [GRN, BLUE, YLW, RED, "#b388ff", "#80deea", "#ff9f43"]
    for i, (sym, df) in enumerate(hists.items()):
        if df is None or df.empty:
            continue
        if mode == "normalized":
            y = df["Close"] / df["Close"].iloc[0] * 100
        elif mode == "returns":
            y = df["Close"].pct_change().fillna(0).cumsum() * 100
        else:
            y = df["Close"]
        fig.add_trace(go.Scatter(x=df.index, y=y, name=sym, mode="lines",
            line=dict(color=palette[i % len(palette)], width=2)))

    layout = BASE.copy()
    layout.update(height=420)
    fig.update_layout(**layout)
    return fig


def corr_heatmap(hists: dict):
    closes = pd.DataFrame({s: d["Close"] for s, d in hists.items() if d is not None and not d.empty})
    corr = closes.pct_change().corr()
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
        colorscale=[[0, RED], [0.5, BG2], [1, GRN]],
        zmid=0, text=corr.round(2).values, texttemplate="%{text}",
    ))
    layout = BASE.copy()
    layout.update(height=380)
    fig.update_layout(**layout)
    return fig
