import streamlit as st

def inject():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg:       #080c10;
    --bg2:      #0e1419;
    --bg3:      #141c24;
    --border:   rgba(255,255,255,0.07);
    --green:    #00d084;
    --red:      #ff4d6d;
    --blue:     #3b9eff;
    --yellow:   #f5c518;
    --text:     #e8edf2;
    --muted:    #5a6a7a;
    --glow:     rgba(0,208,132,0.12);
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"],
[data-testid="stMain"], .main {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: var(--bg2) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

section[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

h1,h2,h3,h4 { font-family: 'Inter', sans-serif !important; font-weight: 700 !important; color: var(--text) !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg3) !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 2px var(--glow) !important;
    outline: none !important;
}

.stSelectbox > div > div { background: var(--bg3) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }
.stSelectbox svg { color: var(--muted) !important; }

.stButton > button {
    background: var(--green) !important;
    color: #060a0d !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
    transition: opacity .15s, transform .15s !important;
}
.stButton > button:hover { opacity: .88 !important; transform: translateY(-1px) !important; }

.stTabs [data-baseweb="tab-list"] { background: transparent !important; border-bottom: 1px solid var(--border) !important; gap: 0 !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--muted) !important; font-family: 'Inter', sans-serif !important; font-size: 13px !important; font-weight: 500 !important; padding: 10px 20px !important; border-bottom: 2px solid transparent !important; }
.stTabs [aria-selected="true"] { color: var(--green) !important; border-bottom: 2px solid var(--green) !important; background: transparent !important; }

[data-testid="stMetric"] { background: var(--bg2); border: 1px solid var(--border); border-radius: 10px; padding: 16px !important; }
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: .06em; }
[data-testid="stMetricValue"] { color: var(--text) !important; font-size: 22px !important; font-weight: 700 !important; }
[data-testid="stMetricDelta"] svg { display: none; }

div[data-testid="stExpander"] { background: var(--bg2) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }

.stRadio > div { gap: 6px !important; }
.stRadio label { font-size: 14px !important; color: var(--text) !important; }

.stMultiSelect > div > div { background: var(--bg3) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; }

hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

.pill {
    display: inline-block;
    background: rgba(0,208,132,0.1);
    border: 1px solid rgba(0,208,132,0.25);
    color: var(--green);
    font-size: 11px;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    letter-spacing: .04em;
    text-transform: uppercase;
}

.card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
}

.muted { color: var(--muted); font-size: 12px; }

.user-msg {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 14px 14px 2px 14px;
    padding: 12px 16px;
    font-size: 14px;
    max-width: 78%;
    margin-left: auto;
    margin-bottom: 12px;
    line-height: 1.6;
}

.ai-msg {
    background: linear-gradient(135deg, rgba(0,208,132,.04), rgba(59,158,255,.04));
    border: 1px solid rgba(0,208,132,.15);
    border-radius: 2px 14px 14px 14px;
    padding: 14px 16px;
    font-size: 14px;
    max-width: 88%;
    margin-bottom: 12px;
    line-height: 1.7;
}

.ai-label { color: var(--green); font-size: 10px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; margin-bottom: 8px; }
.up   { color: var(--green); }
.down { color: var(--red);   }
.flat { color: var(--yellow);}
</style>
""", unsafe_allow_html=True)
