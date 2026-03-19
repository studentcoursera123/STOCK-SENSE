import streamlit as st
from utils.data import fetch, add_indicators
from utils.charts import candle, line, macd_chart
from utils.ai import chat
from utils.data import build_context

def render():
    st.markdown("<div style='font-size:22px;font-weight:700;margin-bottom:20px'>Technical Charts</div>",
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        sym = st.text_input("", placeholder="NSE symbol (e.g. TATAMOTORS, BAJFINANCE)",
                            label_visibility="collapsed", key="chart_sym").upper().strip()
    with col2:
        period = st.selectbox("", ["1mo","3mo","6mo","1y","2y"], index=2,
                              label_visibility="collapsed", key="chart_period")
    with col3:
        chart_type = st.selectbox("", ["Candlestick", "Line", "MACD"],
                                  label_visibility="collapsed", key="chart_type")

    if not sym:
        sym = (st.session_state.get("watchlist") or ["RELIANCE"])[0]

    with st.spinner(f"Loading {sym}…"):
        info, hist = fetch(sym, period)

    if hist is None:
        st.error(f"Could not load **{sym}**.")
        return

    hist = add_indicators(hist)

    if chart_type == "Candlestick":
        c1, c2 = st.columns(2)
        bb  = c1.checkbox("Bollinger Bands", value=True)
        ema = c2.checkbox("EMA 20/50",       value=True)
        st.plotly_chart(candle(hist, sym, bb, ema),
                        use_container_width=True, config={"displayModeBar": False})
    elif chart_type == "Line":
        st.plotly_chart(line(hist, sym),
                        use_container_width=True, config={"displayModeBar": False})
    else:
        st.plotly_chart(macd_chart(hist, sym),
                        use_container_width=True, config={"displayModeBar": False})

    st.markdown("<br>", unsafe_allow_html=True)
    col_q, col_b = st.columns([5, 1])
    with col_q:
        q = st.text_input("", placeholder=f"Ask AI to interpret the {sym} chart…",
                          key="chart_q", label_visibility="collapsed")
    with col_b:
        ask = st.button("Ask", use_container_width=True, key="chart_ask")

    if ask and q:
        ctx = build_context(sym, info, hist)
        with st.spinner(""):
            ans = chat([{"role": "user", "content": f"{ctx}\n\n{q}"}])
        st.markdown(f"""
        <div class='ai-msg' style='margin-top:16px'>
            <div class='ai-label'>StockSense AI</div>
            {ans.replace(chr(10), '<br>')}
        </div>""", unsafe_allow_html=True)
