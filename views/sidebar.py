import streamlit as st
from config.keys import is_configured
from utils.data import TOP_STOCKS

def render():
    with st.sidebar:
        st.markdown("""
        <div style='margin-bottom:28px'>
            <div style='font-size:20px;font-weight:700;color:#00d084;letter-spacing:-.01em'>
                StockSense
            </div>
            <div style='font-size:11px;color:#5a6a7a;margin-top:2px'>
                NSE · BSE · India
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_configured():
            st.markdown("<div class='pill'>● Groq connected</div>", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background:rgba(255,77,109,.08);border:1px solid rgba(255,77,109,.25);
                 border-radius:8px;padding:10px 12px;font-size:12px;color:#ff4d6d'>
                ⚠️ Add <code>GROQ_API_KEY</code> to <code>.env</code>
            </div>""", unsafe_allow_html=True)
            st.caption("[Get free key →](https://console.groq.com)")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:11px;font-weight:600;color:#5a6a7a;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px'>View</div>", unsafe_allow_html=True)
        view = st.radio("", ["Chat", "Markets", "Charts", "Compare"],
                        label_visibility="collapsed", key="view")

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("<div style='font-size:11px;font-weight:600;color:#5a6a7a;letter-spacing:.08em;text-transform:uppercase;margin-bottom:10px'>Watchlist</div>", unsafe_allow_html=True)
        watchlist = st.multiselect("", TOP_STOCKS[:15],
                                   default=["RELIANCE", "TCS", "HDFCBANK"],
                                   label_visibility="collapsed")
        st.session_state["watchlist"] = watchlist

        st.markdown("<hr>", unsafe_allow_html=True)
        st.caption("Data · yfinance\nAI · Groq LLaMA 3.3 70B")

    return view
