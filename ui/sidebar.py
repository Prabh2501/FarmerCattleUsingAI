import streamlit as st

def render_sidebar():
    if "page" not in st.session_state:
        st.session_state.page = "Detection"

    if "profile" not in st.session_state:
        st.session_state.profile = {
            "name": "Not Set",
            "farm": "Not Set",
            "location": "Not Set"
        }

    with st.sidebar:
        st.markdown("## 🚜 Smart Farm OS")

        if st.button("📷 Detection / पहचान", key="det", use_container_width=True):
            st.session_state.page = "Detection"
        if st.button("📊 Dashboard", key="dash", use_container_width=True):
            st.session_state.page = "Dashboard"
        if st.button("🩺 Vet Support", key="vet", use_container_width=True):
            st.session_state.page = "Vet"
        if st.button("🧠 Behavior Analysis", key="beh", use_container_width=True):
            st.session_state.page = "Behavior"
        if st.button("⚙ Settings / सेटिंग्स", key="set", use_container_width=True):
            st.session_state.page = "Settings"

        st.markdown("---")
        st.markdown("### 👨‍🌾 Farmer Profile")

        p = st.session_state.profile
        st.markdown(f"""
        <div class="profile-box">
        <b>Name:</b> {p['name']}<br>
        <b>Farm:</b> {p['farm']}<br>
        <b>Location:</b> {p['location']}
        </div>
        """, unsafe_allow_html=True)
