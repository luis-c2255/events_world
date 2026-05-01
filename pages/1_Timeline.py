import streamlit as st
from components.timeline_html import build_timeline_html
from data.events import EVENTS, LINKS, CATEGORIES


st.set_page_config(layout="wide")
st.title("📜 Interactive Timeline")

html = build_timeline_html(EVENTS, LINKS, CATEGORIES)

st.iframe(html, height=800)

