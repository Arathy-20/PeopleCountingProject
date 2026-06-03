"""
CrowdSense — AI Crowd Estimation
UI  : Compact dark SaaS (Linear/Vercel style)
ML  : CNN Regression · TensorFlow/Keras · ShanghaiTech Part_A dataset
"""
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

st.error("APP IS RUNNING")

from ui.hero import render_hero
from ui.uploader import render_upload
from ui.results import render_results
from ui.styles import load_css

from src.predict import classify_density
from src.load_model import load_model
from src.preprocess import preprocess_image

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CrowdSense · AI Crowd Estimation",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="collapsed",
)

load_css()

st.markdown('<div class="cs-bg"></div>', unsafe_allow_html=True)
st.markdown('<div class="cs-page">', unsafe_allow_html=True)

render_hero()

model = load_model()

if model is None:
    st.markdown(
    '''
    <div class="cs-error">
        ⚠️ <strong>Model not found.</strong><br>
        Place <code>models/people_counter.h5</code> in the models folder.
    </div>
    ''',
    unsafe_allow_html=True,
)
    st.stop()

uploaded_file = render_upload()

if uploaded_file is not None:


    render_results(
        uploaded_file,
        model,
        preprocess_image,
        classify_density
    )

st.markdown(
    '<div class="cs-footer">Powered by CNN • TensorFlow • OpenCV</div>',
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)  # cs-page