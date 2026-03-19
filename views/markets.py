import streamlit as st
from utils.data import fetch, add_indicators, fetch_indices, fmt_crore, TOP_STOCKS
from utils.ai import chat

def render():
    st.markdown("<div style='font-size:22px;font-weight:700;margin-bottom:20px'>Market Overview</div>",
                unsafe_allow_html=True)

    with st.spinner("Loading indices…"):
        indices = fetch_indices()

    if indices:
        cols = st.columns(len(indices))
        for i, (name, d) in enumerate(indices.items()):
            css = "up" if d["chg"] >= 0 else "down"
            with cols[i]:
                st.markdown(f"""
                <div class='card' style='text-align:center'>
                    <div class='muted'>{name}</div>
                    <div style='font-size:22px;font-weight:700;margin:6px 0'>
                        {d['price']:,.2f}
                    </div>
                    <div class='{css}'>{d['chg']:+.2f}%</div>
                </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div style='font-size:15px;font-weight:600;margin-bottom:14px'>Quick Stock Lookup</div>",
                unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        sym = st.text_input("", placeholder="NSE symbol (e.g. RELIANCE, TCS, INFY)",
                            label_visibility="collapsed", key="mkt_sym").upper().strip()
    with col2:
        period = st.selectbox("", ["1mo","3mo","6mo","1y","2y"], index=2,
                              label_visibility="collapsed")

    if not sym:
        sym = (st.session_state.get("watchlist") or ["RELIANCE"])[0]

    with st.spinner(f"Fetching {sym}…"):
        info, hist = fetch(sym, period)

    if hist is None:
        st.error(f"Could not load **{sym}**. Use a valid NSE symbol.")
        return

    hist = add_indicators(hist)
    cur   = hist["Close"].iloc[-1]
    prev  = hist["Close"].iloc[-2] if len(hist) > 1 else cur
    chg   = (cur / prev - 1) * 100
    w_chg = (cur / hist["Close"].iloc[-5]  - 1) * 100 if len(hist) > 5  else 0
    m_chg = (cur / hist["Close"].iloc[-21] - 1) * 100 if len(hist) > 21 else 0
    rsi   = hist["RSI"].iloc[-1] if "RSI" in hist.columns else None

    c1, c2, c3, c4 = st.columns(4)
    def mcard(col, label, val, delta=None, css=""):
        with col:
            dcss = "up" if delta and delta >= 0 else "down" if delta else ""
            d_html = f"<div class='{dcss}' style='font-size:12px;margin-top:4px'>{delta:+.2f}%</div>" if delta is not None else ""
            col.markdown(f"""
            <div class='card' style='text-align:center'>
                <div class='muted'>{label}</div>
                <div style='font-size:20px;font-weight:700;margin:6px 0;{css}'>{val}</div>
                {d_html}
            </div>""", unsafe_allow_html=True)

    mcard(c1, "Price", f"₹{cur:,.2f}", chg)
    mcard(c2, "1-Week", f"{w_chg:+.2f}%", w_chg)
    mcard(c3, "1-Month", f"{m_chg:+.2f}%", m_chg)
    if rsi:
        r_css = "color:#ff4d6d" if rsi > 70 else "color:#00d084" if rsi < 30 else ""
        mcard(c4, "RSI (14)", f"{rsi:.1f}", css=r_css)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div style='font-size:13px;font-weight:600;margin-bottom:12px'>Company Info</div>",
                    unsafe_allow_html=True)
        rows = [("Name", info.get("longName","—")), ("Sector", info.get("sector","—")),
                ("Industry", info.get("industry","—")), ("Exchange", info.get("exchange","—"))]
        for k, v in rows:
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;"
                        f"border-bottom:1px solid rgba(255,255,255,.05)'>"
                        f"<span class='muted'>{k}</span><span style='font-size:13px'>{v}</span></div>",
                        unsafe_allow_html=True)
    with col_r:
        st.markdown("<div style='font-size:13px;font-weight:600;margin-bottom:12px'>Key Metrics</div>",
                    unsafe_allow_html=True)
        pe  = info.get("trailingPE")
        fpe = info.get("forwardPE")
        pm  = info.get("profitMargins")
        dy  = info.get("dividendYield")
        rows = [
            ("Market Cap",    fmt_crore(info.get("marketCap","N/A"))),
            ("P/E",           f"{pe:.1f}" if isinstance(pe, float) else "N/A"),
            ("Forward P/E",   f"{fpe:.1f}" if isinstance(fpe, float) else "N/A"),
            ("Profit Margin", f"{pm*100:.1f}%" if isinstance(pm, float) else "N/A"),
            ("Dividend Yield",f"{dy*100:.2f}%" if isinstance(dy, float) else "N/A"),
            ("Beta",          str(round(info.get("beta",0), 2)) if info.get("beta") else "N/A"),
        ]
        for k, v in rows:
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:6px 0;"
                        f"border-bottom:1px solid rgba(255,255,255,.05)'>"
                        f"<span class='muted'>{k}</span><span style='font-size:13px'>{v}</span></div>",
                        unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_q, col_b = st.columns([5, 1])
    with col_q:
        q = st.text_input("", placeholder=f"Ask AI about {sym}…",
                          key="mkt_q", label_visibility="collapsed")
    with col_b:
        ask = st.button("Ask", use_container_width=True, key="mkt_ask")

    if ask and q:
        ctx = f"Stock data:\n{build_context_inline(sym, info, hist)}"
        with st.spinner(""):
            ans = chat([{"role": "user", "content": f"{ctx}\n\n{q}"}])
        st.markdown(f"""
        <div class='ai-msg' style='margin-top:16px'>
            <div class='ai-label'>StockSense AI</div>
            {ans.replace(chr(10), '<br>')}
        </div>""", unsafe_allow_html=True)


def build_context_inline(sym, info, df):
    from utils.data import build_context
    return build_context(sym, info, df)
