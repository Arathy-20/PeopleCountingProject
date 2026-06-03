import streamlit as st


def render_upload():

    st.markdown("""
    <div class="cs-upload-title-wrap">
        <h2>📤 Upload Crowd Image</h2>
        <p>
            Drag & drop a crowd image or browse files to begin AI analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is None:

        st.markdown("""
        <div class="cs-empty-card">
            <div class="cs-empty-icon">
                🖼️
            </div>
            <div class="cs-empty-title">
                No Image Selected
            </div>
            <div class="cs-empty-text">
                Upload a crowd scene to generate an AI-powered
                crowd estimate.
            </div>
            <div class="cs-empty-support">
                JPG • PNG • JPEG
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    return uploaded_file