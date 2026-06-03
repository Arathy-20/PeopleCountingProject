
import io
import numpy as np
from PIL import Image, UnidentifiedImageError
import streamlit as st

def predict_crowd(
    pil_image,
    model,
    preprocess_image
):
    try:
        img_tensor = preprocess_image(pil_image)

        with st.spinner("Analysing image…"):
            raw_pred = model.predict(
                img_tensor,
                verbose=0
            )

            return max(
                0.0,
                float(np.squeeze(raw_pred))
            )

    except Exception as exc:

        st.markdown(
            f'''
            <div class="cs-error">
            ❌ Prediction failed: {exc}
            </div>
            ''',
            unsafe_allow_html=True
        )

        return None

def render_results(
    uploaded_file,
    model,
    preprocess_image,
    classify_density
): 
    # ── Hide the uploader widget via CSS injection once file exists ──────────
    st.markdown("""
    <style>
    [data-testid="stFileUploader"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    pil_image = validate_image(uploaded_file)
    if pil_image is None:
        return

    crowd_count = predict_crowd(
    pil_image,
    model,
    preprocess_image
)

    if crowd_count is None:
        return

    # ── Derive display values ─────────────────────────────────────────────────
    density_label, badge_class, density_emoji = classify_density(crowd_count)
    count_display = int(round(crowd_count))

    if crowd_count < 50:
        ring_color = "#3FB950"
        insight    = "Light pedestrian activity detected."
    elif crowd_count < 200:
        ring_color = "#D29922"
        insight    = "Moderate crowd concentration detected."
    else:
        ring_color = "#F85149"
        insight    = "High pedestrian concentration detected."

    # ── Two-column results dashboard ──────────────────────────────────────────
    st.markdown('<div class="cs-results">', unsafe_allow_html=True)
    col_img, col_pred = st.columns([1.15, 0.85], gap="large")

    with col_img:
        with st.container(border=True):
            st.markdown(
                    '<p class="cs-image-label">Uploaded Image</p>',
                    unsafe_allow_html=True
            )


            left, center, right = st.columns([1, 4, 1])

            with center:
                st.image(
                    pil_image,
                    width=400
                )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

    with col_pred:
        st.markdown(f"""
        <div class="cs-pred-card glass">
            <div class="cs-count-ring" style="
                background: linear-gradient(135deg, {ring_color}, rgba(255,255,255,0.15));
                box-shadow: 0 0 36px {ring_color}40;">
                <div class="cs-count-inner">
                    <span class="cs-count-number">{count_display}</span>
                    <span class="cs-count-unit">People</span>
                </div>
            </div>
            <span class="cs-density-badge {badge_class}">
                {density_emoji}&nbsp;{density_label}
            </span>
            <p class="cs-estimate-note">{insight}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # cs-results

def validate_image(uploaded_file):
    try:
        raw_bytes = uploaded_file.read()
        pil_image = Image.open(io.BytesIO(raw_bytes))
        pil_image.verify()
        pil_image = Image.open(io.BytesIO(raw_bytes))
        return pil_image
    except Exception:
        st.markdown(
            '''
            <div class="cs-error">
            ❌ Invalid image file
            </div>
            ''',
            unsafe_allow_html=True
        )

    return None
