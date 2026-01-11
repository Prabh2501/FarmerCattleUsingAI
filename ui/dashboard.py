import streamlit as st
import pandas as pd

from backend.database import (
    get_all_animals,
    delete_animal,
    update_display_name
)

# Emoji mapping (farmer-friendly)
ANIMAL_EMOJI = {
    "Cow": "🐄",
    "Buffalo": "🐃",
    "Goat": "🐐",
    "Sheep": "🐑",
    "Horse": "🐎",
    "Bird": "🐦"
}

def render_dashboard():
    st.subheader("📊 Farm Dashboard")

    # Load data from backend
    df = get_all_animals()

    if df.empty:
        st.info("No animals recorded yet.")
        return

    # View toggle
    col_toggle, _ = st.columns([1, 5])
    with col_toggle:
        table_view = st.toggle("📋 Table View")

    st.markdown("---")

    # ---------------- TABLE VIEW ----------------
    if table_view:
        table_df = df[
            ["display_name", "animal_type", "health_status", "attendance", "last_seen"]
        ]
        st.dataframe(table_df, use_container_width=True)

    # ---------------- CARD VIEW ----------------
    else:
        cols = st.columns(3)

        for idx, row in df.iterrows():
            with cols[idx % 3]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                emoji = ANIMAL_EMOJI.get(row["animal_type"], "🐾")
                st.markdown(f"### {emoji} {row['display_name']}")

                st.caption(f"Type: {row['animal_type']}")
                st.caption(f"Attendance: {row['attendance']}")
                st.caption(f"Last seen: {row['last_seen']}")

                if row["health_status"] == "Healthy":
                    st.markdown(
                        "<div class='badge-green'>✅ Healthy</div>",
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        "<div class='badge-red'>🚨 Needs Vet Support</div>",
                        unsafe_allow_html=True
                    )
                    st.button(
                        "📍 Find Nearest Vet",
                        key=f"vet_{row['animal_id']}"
                    )

                # Rename animal
                new_name = st.text_input(
                    "Rename",
                    value=row["display_name"],
                    key=f"name_{row['animal_id']}"
                )

                if new_name != row["display_name"]:
                    update_display_name(row["animal_id"], new_name)

                # Delete animal
                if st.button("❌ Delete", key=f"del_{row['animal_id']}"):
                    delete_animal(row["animal_id"])
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)
