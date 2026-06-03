import streamlit as st

def render_hero():

    st.markdown("""
    <div class="cs-hero">
        <h1 class="cs-hero-title">👥 CrowdSense</h1>
        <p class="cs-hero-sub">
            AI-Powered Crowd Estimation
        </p>
    </div>
    """, unsafe_allow_html=True)