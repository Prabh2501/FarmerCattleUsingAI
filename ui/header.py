import streamlit as st

def render_header(language="English"):
    title = "🌱 Farm Management" if language == "English" else "🌱 फार्म प्रबंधन"
    subtitle = "LIVE" if language == "English" else "लाइव"

    st.markdown(f"""
    <div class="header">
        <h2>{title} <span style="font-size:14px; background:#bbf7d0; color:#166534; padding:4px 10px; border-radius:10px;">{subtitle}</span></h2>
        <p>Smart monitoring for livestock</p>
    </div>
    """, unsafe_allow_html=True)
