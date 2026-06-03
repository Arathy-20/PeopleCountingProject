import streamlit as st
import tensorflow as tf

MODEL_PATH = "models/people_counter.h5"

@st.cache_resource(show_spinner=False)
def load_model():
    return tf.keras.models.load_model(MODEL_PATH)