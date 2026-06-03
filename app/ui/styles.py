import streamlit as st

def load_css():
    
    st.markdown("""
    <style>
   /* @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap'); */

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html, body, [class*="css"], .stApp {
        font-family: 'Outfit', sans-serif;
        background: #060a18;
        color: #E6EDF3;
    }

    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header,
    section[data-testid="stSidebar"],
    .stDeployButton,
    div[data-testid="stToolbar"] { display: none !important; }

    /* ── Remove default block padding ── */
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* ── Subtle ambient background ── */
    .cs-bg {
        position: fixed; inset: 0; z-index: 0;
        background: #060a18; pointer-events: none; overflow: hidden;
    }
    .cs-bg::before {
        content: '';
        position: absolute; top: -20%; left: -10%; width: 55%; height: 55%;
        background: radial-gradient(ellipse, rgba(88,166,255,0.07) 0%, transparent 70%);
        animation: drift1 14s ease-in-out infinite alternate;
    }
    .cs-bg::after {
        content: '';
        position: absolute; bottom: -15%; right: -10%; width: 50%; height: 50%;
        background: radial-gradient(ellipse, rgba(63,185,80,0.06) 0%, transparent 70%);
        animation: drift2 18s ease-in-out infinite alternate;
    }

    @keyframes drift1 { from{transform:translate(0,0)} to{transform:translate(5%,6%)} }
    @keyframes drift2 { from{transform:translate(0,0)} to{transform:translate(-4%,-5%)} }
    @keyframes fadeUp { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:translateY(0)} }
    @keyframes pulse  { 0%,100%{opacity:1} 50%{opacity:0.3} }
    @keyframes ringIn { from{transform:scale(0.75);opacity:0} to{transform:scale(1);opacity:1} }

    /* ── Page wrapper ── */
    .cs-page {
        position: relative; z-index: 1;
        width: 100%; max-width: 1100px;
        margin: 0 auto;
        padding: 1rem 2rem 0.5rem;
        display: flex; flex-direction: column; align-items: center;
    }

    /* ── Compact Hero ── */
    .cs-hero{
    text-align:center;
    margin-bottom:2rem;
}

.cs-hero-title{
    font-size:3.5rem;
    font-weight:700;
    margin-bottom:0.5rem;
}

.cs-hero-sub{
    color:#8B949E;
    font-size:1rem;
}

    /* ── Glassmorphism base ── */
    .glass {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
    }

    /* ── Upload section label ── */
    .cs-upload-header {
        padding: 1.25rem 1.4rem 1rem;
        text-align: center;
        border-bottom: none;
    }

    .cs-upload-title {
        font-size: 1rem;
        font-weight: 700;
        color: #E6EDF3;
        margin-bottom: 0.3rem;
    }

    .cs-upload-hint {
        font-size: 0.8rem;
        color: #8B949E;
    }

    .cs-upload-title-wrap{
    text-align:center;
    margin-bottom:1rem;
    }

    .cs-upload-title-wrap h2{
        margin-bottom:0.5rem;
    }

    .cs-upload-title-wrap p{
        color:#8B949E;
        margin:0;
    }

    /* ── Upload Zone ── */

    .stFileUploader label {
        display: none !important;
    }

    [data-testid="stFileUploader"] {
        width: 100%;
        max-width: 750px;
        margin: 0 auto;
    }

    [data-testid="stFileUploaderDropzone"] {
        min-height: 220px !important;
        background: rgba(255,255,255,0.03) !important;
        border: 2px dashed rgba(88,166,255,0.35) !important;
        border-radius: 20px !important;
        backdrop-filter: blur(20px);

        display: flex;
        align-items: center;
        justify-content: center;

        transition: all 0.3s ease;
    }

    [data-testid="stFileUploaderDropzone"]::before {
        content: "📤";
        font-size: 2rem;
        display: block;
        margin-bottom: 10px;
    }

    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #58A6FF !important;
        background: rgba(88,166,255,0.05) !important;
        transform: translateY(-2px);
        box-shadow: 0 0 25px rgba(88,166,255,0.15);
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        display: none !important;
    }

    /* ─────────────────────────────────────────────
    Empty State Card
    ───────────────────────────────────────────── */

    .cs-empty-card{
        max-width:700px;
        margin:2rem auto;

        padding:2.5rem;
        text-align:center;
        background:rgba(255,255,255,0.03);
        border:1px solid rgba(255,255,255,0.08);
        border-radius:24px;
        backdrop-filter:blur(12px);
        box-shadow:
            0 8px 32px rgba(0,0,0,0.25);
        transition:all 0.3s ease;
    }

    .cs-empty-card:hover{
        border-color:rgba(88,166,255,0.25);
        transform:translateY(-2px);
    }

    .cs-empty-icon{
        font-size:4rem;
        margin-bottom:1rem;
    }

    .cs-empty-title{
        font-size:1.5rem;
        font-weight:700;
        color:#E6EDF3;
        margin-bottom:0.75rem;
    }

    .cs-empty-text{
        max-width:500px;
        margin:0 auto 1.25rem auto;
        color:#8B949E;
        line-height:1.6;
    }

    .cs-empty-support{
        display:inline-block;
        padding:0.45rem 0.9rem;
        border-radius:999px;
        background:rgba(88,166,255,0.12);
        border:1px solid rgba(88,166,255,0.2);
        color:#58A6FF;
        font-size:0.85rem;
        font-weight:500;
    }

    /* ── Results wrapper ── */
    .cs-results {
        width: 100%;
        max-width: 1100px;
        margin: 0 auto;
        animation: fadeUp 0.55s cubic-bezier(.16,1,.3,1) both;
    }

    /* ── Image card ── */
    .cs-image-card {
        padding: 1.25rem;
        border-radius: 20px;
        min-height: 500px;
    }
    
    div[data-testid="stVerticalBlock"] .cs-image-label{
        font-size:0.65rem;
        font-weight:700;
        letter-spacing:0.14em;
        text-transform:uppercase;
        color:#8B949E;
    }
                
    
                
    /* ── Prediction card ── */
    .cs-pred-card {
        padding: 2rem 1.5rem;
        border-radius: 18px;
        text-align: center;
        height: 100%;
        position: relative;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 1.2rem;
    }
    .cs-pred-card::before {
        content: '';
        position: absolute; top: -50%; left: 50%; transform: translateX(-50%);
        width: 80%; height: 80%;
        background: radial-gradient(ellipse, rgba(88,166,255,0.09) 0%, transparent 70%);
        pointer-events: none;
    }

    /* ── Count ring ── */
    .cs-count-ring {
        width: 180px; height: 180px;
        border-radius: 50%; padding: 3px;
        box-shadow: 0 0 32px rgba(88,166,255,0.2);
        animation: ringIn 0.5s cubic-bezier(.16,1,.3,1) both;
    }
    .cs-count-inner {
        width: 100%; height: 100%; border-radius: 50%;
        background: rgba(6,10,24,0.93);
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        border: 1px solid rgba(88,166,255,0.1);
    }
    .cs-count-number {
        font-size: 3.6rem; font-weight: 900; line-height: 1; letter-spacing: -2px;
        background: linear-gradient(135deg, #E6EDF3, #58A6FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    }
    .cs-count-unit {
        font-size: 0.6rem; font-weight: 700;
        letter-spacing: 0.22em; text-transform: uppercase;
        color: #8B949E; margin-top: 0.2rem;
    }

    /* ── Density badges ── */
    .cs-density-badge {
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.45rem 1.2rem; border-radius: 999px;
        font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em;
        animation: fadeUp 0.5s cubic-bezier(.16,1,.3,1) 0.2s both;
        transition: transform 0.2s;
    }
    .cs-density-badge:hover { transform: translateY(-2px); }
    .cs-badge-light    { background:rgba(63,185,80,0.11);  border:1px solid rgba(63,185,80,0.32);  color:#3FB950; }
    .cs-badge-moderate { background:rgba(210,153,34,0.11); border:1px solid rgba(210,153,34,0.32); color:#D29922; }
    .cs-badge-heavy    { background:rgba(248,81,73,0.11);  border:1px solid rgba(248,81,73,0.32);  color:#F85149; }

    .cs-estimate-note {
        font-size: 0.76rem;
        color: rgba(139,148,158,0.6);
        line-height: 1.6; max-width: 240px;
        text-align: center;
    }

    /* ── Error ── */
    .cs-error {
        max-width: 520px; margin: 1.5rem auto; padding: 1.2rem 1.8rem;
        border-radius: 14px;
        background: rgba(248,81,73,0.08); border: 1px solid rgba(248,81,73,0.25);
        color: #F85149; font-size: 0.88rem; text-align: center;
    }

    /* ── Footer ── */
    .cs-footer {
        margin-top: 1rem; padding-top: 0.5rem; text-align: center;
        font-size: 0.72rem; color: rgba(139,148,158,0.35);
        letter-spacing: 0.06em;
    }

    /* ── Image display ── */
    .stImage img {
        border-radius: 12px;
        width: 100% !important;
        object-fit: cover;
        box-shadow: 0 12px 40px rgba(0,0,0,0.45), 0 0 0 1px rgba(255,255,255,0.04);
    }

    /* ── Spinner ── */
    .stSpinner > div {
        border-color: #58A6FF transparent transparent transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)