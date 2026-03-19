import streamlit as st
from utils.ai import stream
from utils.data import fetch, add_indicators, build_context

SUGGESTIONS = [
    "Analyse Reliance Industries for me",
    "Which Nifty 50 stocks look oversold right now?",
    "Explain how FII flows impact Indian markets",
    "Compare TCS vs Infosys fundamentals",
    "What does RBI rate hike mean for banking stocks?",
    "Is HDFC Bank a good long-term buy?",
]


def _context_for(symbols: list) -> str:
    parts = []
    for s in symbols[:3]:
        info, hist = fetch(s)
        if hist is not None:
            hist = add_indicators(hist)
            parts.append(build_context(s, info, hist))
    return "\n\n---\n\n".join(parts)


def render():
    st.markdown("""
    <div style='margin-bottom:28px'>
        <div style='font-size:28px;font-weight:700;line-height:1.15'>
            Ask anything about<br>
            <span style='color:#00d084'>Indian markets</span>
        </div>
        <div style='color:#5a6a7a;font-size:13px;margin-top:8px'>
            Powered by Groq · LLaMA 3.3 70B · NSE/BSE data
        </div>
    </div>
    """, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    watchlist = st.session_state.get("watchlist", [])

    if not st.session_state["messages"]:
        st.markdown("<div style='color:#5a6a7a;font-size:12px;margin-bottom:12px'>Try asking:</div>",
                    unsafe_allow_html=True)
        cols = st.columns(2)
        for i, s in enumerate(SUGGESTIONS):
            if cols[i % 2].button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state["pending"] = s
                st.rerun()
    else:
        for m in st.session_state["messages"]:
            if m["role"] == "user":
                st.markdown(f"<div class='user-msg'>{m['content']}</div>",
                            unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='ai-msg'>
                    <div class='ai-label'>StockSense AI</div>
                    {m['content'].replace(chr(10), '<br>')}
                </div>""", unsafe_allow_html=True)

    pending = st.session_state.pop("pending", None)

    col_inp, col_btn = st.columns([6, 1])
    with col_inp:
        user_input = st.text_input("", value=pending or "",
                                   placeholder="Ask about any NSE/BSE stock or market topic…",
                                   label_visibility="collapsed", key="chat_input")
    with col_btn:
        send = st.button("Send", use_container_width=True)

    if (send or pending) and (user_input or pending):
        msg = user_input or pending
        st.session_state["messages"].append({"role": "user", "content": msg})

        context = _context_for(watchlist) if watchlist else ""
        history = [{"role": m["role"], "content": m["content"]}
                   for m in st.session_state["messages"][:-1]]
        prompt_msg = {"role": "user", "content": f"{context}\n\n{msg}".strip() if context else msg}

        with st.spinner(""):
            response = "".join(stream(history + [prompt_msg]))

        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.rerun()

    if st.session_state["messages"]:
        if st.button("Clear conversation", key="clear"):
            st.session_state["messages"] = []
            st.rerun()
