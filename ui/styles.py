import streamlit as st

def load_styles():
    st.markdown("""
    <style>

    /* -------- GLOBAL RESET -------- */
    html, body, [class*="css"]  {
        background-color: #f9fafb !important;
        color: #111827 !important;
    }

    /* -------- MAIN APP AREA -------- */
    section.main > div {
        background-color: #f9fafb !important;
        padding: 0rem 1.5rem;
    }

    /* -------- SIDEBAR -------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16a34a, #15803d) !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* -------- HEADER -------- */
    .header {
        background: linear-gradient(90deg, #16a34a, #22c55e);
        padding: 24px;
        border-radius: 18px;
        color: white;
        margin-bottom: 20px;
    }

    /* -------- CARDS -------- */
    .card {
        background-color: #ffffff !important;
        padding: 18px;
        border-radius: 18px;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
        color: #111827 !important;
    }

    /* -------- BADGES -------- */
    .badge-green {
        background-color: #dcfce7;
        color: #166534 !important;
        padding: 6px 12px;
        border-radius: 10px;
        font-weight: bold;
    }

    .badge-red {
        background-color: #fee2e2;
        color: #991b1b !important;
        padding: 6px 12px;
        border-radius: 10px;
        font-weight: bold;
    }

    /* -------- NAV BUTTONS -------- */
    .nav-btn {
        width: 100%;
        background-color: rgba(255,255,255,0.18);
        color: white !important;
        padding: 14px;
        border-radius: 12px;
        border: none;
        margin-bottom: 8px;
        font-size: 16px;
        text-align: left;
    }

    .nav-btn:hover {
        background-color: rgba(255,255,255,0.28);
    }

    /* -------- PROFILE BOX -------- */
    .profile-box {
        background-color: rgba(255,255,255,0.22);
        padding: 12px;
        border-radius: 12px;
        margin-top: 20px;
        color: white !important;
    }

    /* -------- STREAMLIT WIDGET FIXES -------- */
    input, textarea, select {
        background-color: #ffffff !important;
        color: #111827 !important;
    }

    button {
        background-color: #22c55e !important;
        color: white !important;
        border-radius: 10px !important;
    }

    </style>
    """, unsafe_allow_html=True)
