import streamlit as st
import pandas as pd
from utils.data import fetch, add_indicators, build_context, fmt_crore
from utils.charts import compare, corr_heatmap
from utils.ai import chat

SECTOR_PRESETS = {
    "Banking":  ["HDFCBANK","ICICIBANK","SBIN","KOTAKBANK","AXISBANK"],
    "IT":       ["TCS","INFY","WIPRO","HCLTECH","TECHM"],
    "Auto":     ["MARUTI","TATAMOTORS","HEROMOTOCO","EICHERMOT"],
    "Pharma":   ["SUNPHARMA","DRREDDY","CIPLA","DIVISLAB"],
    "Energy":   ["RELIANCE","ONGC","NTPC","POWERGRID","ADANIENT"],
}

def render():
    st.markdown("<div style='font-size:22px;font-weight:700;margin-bottom:20px'>Compare Stocks</div>",
                unsafe_allow_html=True)

    st.markdown("<div class='muted' style='margin-bottom:8px'>Sector presets</div>",
                unsafe_allow_html=True)
    cols = st.columns(len(SECTOR_PRESETS))
    preset_tickers = []
    for i, (label, tickers) in enumerate(SECTOR_PRESETS.items()):
        if cols[i].button(label, key=f"preset_{i}", use_container_width=True):
            preset_tickers = tickers

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        raw = st.text_input("", value=", ".join(preset_tickers) if preset_tickers else "",
                            placeholder="NSE symbols comma-separated (e.g. RELIANCE, TCS, INFY)",
                            label_visibility="collapsed", key="cmp_input")
    with col2:
        period = st.selectbox("", ["1mo","3mo","6mo","1y","2y"], index=2,
                              label_visibility="collapsed", key="cmp_period")
    with col3:
        mode = st.selectbox("", ["normalized","returns","price"],
                            label_visibility="collapsed", key="cmp_mode",
                            format_func=lambda x: {"normalized":"Normalised","returns":"Returns %","price":"Price ₹"}[x])

    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()][:6]
    if not tickers:
        tickers = ["RELIANCE", "TCS", "INFY"]

    with st.spinner("Loading…"):
        data = {}
        for t in tickers:
            info, hist = fetch(t, period)
            if hist is not None:
                data[t] = (info, add_indicators(hist))

    if not data:
        st.error("Could not load data. Use valid NSE symbols.")
        return

    rows = []
    for sym, (info, hist) in data.items():
        cur   = hist["Close"].iloc[-1]
        prev  = hist["Close"].iloc[-2] if len(hist) > 1 else cur
        m_ago = hist["Close"].iloc[-21] if len(hist) > 21 else cur
        pe    = info.get("trailingPE")
        beta  = info.get("beta")
        rows.append({
            "Symbol":    sym,
            "Price (₹)": f"₹{cur:,.2f}",
            "Day %":     f"{(cur/prev-1)*100:+.2f}%",
            "1M %":      f"{(cur/m_ago-1)*100:+.2f}%",
            "Mkt Cap":   fmt_crore(info.get("marketCap","N/A")),
            "P/E":       f"{pe:.1f}" if isinstance(pe, float) else "N/A",
            "Beta":      f"{beta:.2f}" if isinstance(beta, float) else "N/A",
            "RSI":       f"{hist['RSI'].iloc[-1]:.1f}" if "RSI" in hist.columns else "N/A",
            "Sector":    info.get("sector","N/A"),
        })
    st.dataframe(pd.DataFrame(rows).set_index("Symbol"), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    hists = {s: d[1] for s, d in data.items()}
    st.plotly_chart(compare(hists, mode), use_container_width=True, config={"displayModeBar": False})

    if len(data) >= 2:
        st.plotly_chart(corr_heatmap(hists), use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)
    col_q, col_b = st.columns([5, 1])
    with col_q:
        q = st.text_input("", placeholder="Ask AI to compare these stocks…",
                          key="cmp_q", label_visibility="collapsed")
    with col_b:
        ask = st.button("Ask", use_container_width=True, key="cmp_ask")

    if ask and q:
        ctx = "\n\n---\n\n".join([build_context(s, info, hist) for s, (info, hist) in data.items()])
        with st.spinner(""):
            ans = chat([{"role": "user", "content": f"{ctx}\n\n{q}"}])
        st.markdown(f"""
        <div class='ai-msg' style='margin-top:16px'>
            <div class='ai-label'>StockSense AI</div>
            {ans.replace(chr(10), '<br>')}
        </div>""", unsafe_allow_html=True)
