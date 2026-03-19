import streamlit as st
from config.styles import inject
from views.sidebar import render as sidebar

st.set_page_config(
    page_title="StockSense",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject()
view = sidebar()

if view == "Chat":
    from views.chat import render
elif view == "Markets":
    from views.markets import render
elif view == "Charts":
    from views.charts import render
else:
    from views.compare import render

render()
