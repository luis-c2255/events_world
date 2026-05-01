import streamlit as st

st.set_page_config(page_title="History Explorer", page_icon="🌍", layout="wide")

st.markdown("""
            <div style='text-align: center; padding: 2rem 0 1rem 0;'>
                <h1 style='font-size: 3rem; margin-bottom: 0.25rem;'>🌍 History Explorer</h1>
                <p style='font-size: 1.2rem; color: #9ca3af;'>Understand the events that shaped humanity</p>
                <p style='color: #6b7280; max-width: 600px; margin: 0.5rem auto 0 auto;'>
                    Explore a visual timeline of major historical events.<br>
                    Filter by era, category, and dive deeper into each moment.
                </p>
            </div>
        """, unsafe_allow_html=True)

st.divider()

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
                <div style='text-align:center; padding: 1rem;'>
            <div style='font-size: 2.5rem;'>📜</div>
            <h3>Timeline</h3>
            <p style='color: #9ca3af; font-size: 0.9rem;'>
                Explore major events across human history on an interactive visual timeline.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Timeline", width="stretch", type="primary"):
        st.switch_page("pages/1_Timeline.py")
 
with col2:
    st.markdown("""
        <div style='text-align:center; padding: 1rem;'>
            <div style='font-size: 2.5rem;'>👤</div>
            <h3>Persons</h3>
            <p style='color: #9ca3af; font-size: 0.9rem;'>
                Discover the key historical figures who changed the course of civilization.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Persons", width="stretch", type="secondary"):
        st.switch_page("pages/3_Persons.py")
 
with col3:
    st.markdown("""
        <div style='text-align:center; padding: 1rem;'>
            <div style='font-size: 2.5rem;'>📖</div>
            <h3>About</h3>
            <p style='color: #9ca3af; font-size: 0.9rem;'>
                Learn how to navigate and get the most out of History Explorer.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.button("How to Use", width="stretch", type="secondary", disabled=True)
 
st.divider()
 
# Stats row
e1, e2, e3, e4 = st.columns(4)
with e1:
    st.metric("Historical Events", "36")
with e2:
    st.metric("Time Span", "12,000 years")
with e3:
    st.metric("Historical Figures", "19")
with e4:
    st.metric("Categories", "6")
