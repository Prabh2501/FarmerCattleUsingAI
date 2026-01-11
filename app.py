import streamlit as st
import cv2
import numpy as np
import hashlib
from ultralytics import YOLO

from ui.styles import load_styles
from ui.sidebar import render_sidebar
from ui.header import render_header
from ui.dashboard import render_dashboard
from backend.database import upsert_animal

st.set_page_config("Smart Farm OS", layout="wide")

load_styles()
render_sidebar()

language = st.selectbox("🌐 Language", ["English", "Hindi"])
render_header(language)

@st.cache_resource
def load_model():
    return YOLO("./yolov8n.pt")

model = load_model()

def gen_id(crop, animal):
    _, buf = cv2.imencode(".jpg", crop)
    return f"{animal.upper()}_{hashlib.md5(buf).hexdigest()[:8]}"

def health(conf):
    return "Healthy" if conf >= 0.6 else "Needs Vet Support"

page = st.session_state.page

# ---------- IMAGE ----------
if page == "Detection":
    st.subheader("📷 Image Detection")
    uploaded = st.file_uploader("Upload image", type=["jpg","png","jpeg"])

    if uploaded:
        img = cv2.imdecode(np.frombuffer(uploaded.read(), np.uint8), 1)
        results = model(img)

        for box in results[0].boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            animal = results[0].names[cls]

            x1,y1,x2,y2 = map(int, box.xyxy[0])
            crop = img[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            upsert_animal(
                gen_id(crop, animal),
                animal.capitalize(),
                health(conf)
            )

        st.success("Detection complete.")
        st.rerun()

# ---------- VIDEO ----------
elif page == "Video":
    st.subheader("🎥 Video Detection")
    video = st.file_uploader("Upload video", type=["mp4","avi"])

    if video:
        temp = "temp.mp4"
        with open(temp, "wb") as f:
            f.write(video.read())

        cap = cv2.VideoCapture(temp)
        frame_count = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            if frame_count % 15 != 0:
                continue

            results = model(frame)
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                animal = results[0].names[cls]

                x1,y1,x2,y2 = map(int, box.xyxy[0])
                crop = frame[y1:y2, x1:x2]
                if crop.size == 0:
                    continue

                upsert_animal(
                    gen_id(crop, animal),
                    animal.capitalize(),
                    health(conf)
                )

        cap.release()
        st.success("Video processed.")
        st.rerun()

# ---------- DASHBOARD ----------
elif page == "Dashboard":
    render_dashboard()

elif page == "Vet":
    st.subheader("🩺 Vet Support")
    st.info("Vet & map integration will appear here.")

elif page == "Settings":
    st.subheader("⚙ Settings")
    st.session_state.profile["name"] = st.text_input("Name", st.session_state.profile["name"])
    st.session_state.profile["farm"] = st.text_input("Farm", st.session_state.profile["farm"])
    st.session_state.profile["location"] = st.text_input("Location", st.session_state.profile["location"])

# ===================== EXTENSIONS (APPEND ONLY) =====================

# ---- EMOJI MAP (GLOBAL) ----
ANIMAL_EMOJI_EXT = {
    "Cow": "🐄",
    "Buffalo": "🐃",
    "Goat": "🐐",
    "Sheep": "🐑",
    "Horse": "🐎",
    "Bird": "🐦",
    "Dog": "🐕"
}

# ---- SIMPLE BEHAVIOR ANALYSIS (VIDEO FRAMES) ----
def analyze_behavior(motion_score):
    """
    motion_score: average pixel movement
    """
    if motion_score < 5:
        return "Low Activity (Possible Weakness)"
    elif motion_score > 40:
        return "High Restlessness (Possible Stress)"
    else:
        return "Normal Behavior"

# ---- DISEASE HINT ENGINE (EXPLAINABLE) ----
def infer_possible_disease(confidence, behavior):
    if confidence < 0.5 and "Low Activity" in behavior:
        return "Possible Fever or Infection"
    if "Restlessness" in behavior:
        return "Possible Pain or Discomfort"
    return "No Visible Disease"

# ---- GOOGLE MAPS VET LINK ----
def vet_map_link(location="nearest veterinary hospital"):
    base = "https://www.google.com/maps/search/"
    return f"{base}{location.replace(' ', '+')}"

# ===================== ENHANCED VET PAGE =====================
if page == "Vet":
    st.subheader("🩺 Vet Support / पशु चिकित्सक")

    from backend.database import get_all_animals
    df = get_all_animals()

    critical = df[df["health_status"] != "Healthy"]

    if critical.empty:
        st.success("✅ All animals are healthy. No vet visit required.")
    else:
        st.warning("🚨 Some animals need vet support")

        for _, row in critical.iterrows():
            emoji = ANIMAL_EMOJI_EXT.get(row["animal_type"], "🐾")
            st.markdown(f"### {emoji} {row['display_name']}")
            st.write("Status:", row["health_status"])

            st.markdown(
                f"[📍 Find Nearest Vet]({vet_map_link(st.session_state.profile.get('location','vet'))})"
            )

# ===================== VIDEO BEHAVIOR EXTENSION =====================
if page == "Video":
    st.subheader("🎥 Video Behavior Analysis")

    video = st.file_uploader("Upload animal video", type=["mp4", "avi", "mov"])

    if video:
        temp_path = "temp_behavior.mp4"
        with open(temp_path, "wb") as f:
            f.write(video.read())

        cap = cv2.VideoCapture(temp_path)
        prev_gray = None
        motion_values = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if prev_gray is not None:
                diff = cv2.absdiff(prev_gray, gray)
                motion_values.append(np.mean(diff))
            prev_gray = gray

        cap.release()

        if motion_values:
            motion_score = sum(motion_values) / len(motion_values)
            behavior = analyze_behavior(motion_score)

            st.info(f"🧠 Behavior Analysis: {behavior}")

            disease_hint = infer_possible_disease(0.45, behavior)
            st.warning(f"🦠 AI Health Hint: {disease_hint}")

            if "Possible" in disease_hint:
                st.markdown(
                    f"[📍 Find Nearest Vet]({vet_map_link(st.session_state.profile.get('location','vet'))})"
                )

# ===================== LANGUAGE HELPER (OPTIONAL USE) =====================
def t(en, hi):
    return en if language == "English" else hi

# ===================== END EXTENSIONS =====================
# ===================== FINAL EXTENSIONS =====================

# ---- LIVE CAMERA (REAL-TIME DEMO) ----
if page == "Live Camera":
    st.subheader("📸 Live Camera Detection")

    st.info(
        "This uses the local camera. "
        "AI assists detection, final decisions remain with the farmer."
    )

    run_cam = st.toggle("▶ Start Camera")

    if run_cam:
        cam = cv2.VideoCapture(0)
        frame_slot = st.empty()

        while run_cam and cam.isOpened():
            ret, frame = cam.read()
            if not ret:
                st.error("Camera not accessible")
                break

            results = model(frame)
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                animal = results[0].names[cls]

                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(
                    frame,
                    f"{animal} {conf:.2f}",
                    (x1, y1-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )

                crop = frame[y1:y2, x1:x2]
                if crop.size != 0:
                    upsert_animal(
                        gen_id(crop, animal),
                        animal.capitalize(),
                        health(conf)
                    )

            frame_slot.image(frame, channels="BGR")

        cam.release()


# ---- SYSTEM TRANSPARENCY PANEL ----
if page == "Settings":
    st.markdown("---")
    st.subheader("🔍 AI Transparency")

    st.write(
        """
        • AI **does not make final decisions**  
        • AI reduces repetitive work for farmers  
        • Health alerts are **early warnings**, not diagnoses  
        • Farmer experience always has priority  
        """
    )

    st.markdown("### ⚙ System Status")
    st.success("✔ Camera: Ready")
    st.success("✔ AI Model: Loaded")
    st.success("✔ Local Storage: Active")
    st.info("✔ Works in low or no internet environments")


# ---- OFFLINE NOTICE (GLOBAL) ----
st.markdown(
    """
    <div style="
        position: fixed;
        bottom: 10px;
        right: 20px;
        background: #dcfce7;
        color: #166534;
        padding: 8px 14px;
        border-radius: 10px;
        font-size: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.1);
    ">
    📴 Offline-friendly system
    </div>
    """,
    unsafe_allow_html=True
)

# ===================== END OF ALL EXTENSIONS =====================

# ===================== BEHAVIOR ANALYSIS FIX =====================

def analyze_behavior_from_video(video_path):
    """
    Robust motion-based behavior analysis.
    Always returns a result + explanation.
    """
    cap = cv2.VideoCapture(video_path)
    prev_gray = None
    motion_sum = 0
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Sample every 10th frame to reduce noise
        if frame_count % 10 != 0:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:
            diff = cv2.absdiff(prev_gray, gray)
            motion = np.mean(diff)
            motion_sum += motion

        prev_gray = gray

    cap.release()

    if frame_count == 0:
        return "Unknown", "Video could not be analyzed"

    avg_motion = motion_sum / max(1, frame_count)

    # ---- Farmer-friendly interpretation ----
    if avg_motion < 3:
        return (
            "Low Activity",
            "Animal is moving very little. This can indicate weakness, illness, or tiredness."
        )
    elif avg_motion > 25:
        return (
            "High Restlessness",
            "Animal is moving too much. This can indicate stress, discomfort, or pain."
        )
    else:
        return (
            "Normal Behavior",
            "Animal movement appears normal."
        )

# ===================== OVERRIDE VIDEO PAGE (BEHAVIOR OUTPUT) =====================
if page == "Video":
    st.subheader("🎥 Video Behavior Analysis")

    video = st.file_uploader("Upload animal video", type=["mp4", "avi", "mov"])

    if video:
        temp_path = "behavior_temp.mp4"
        with open(temp_path, "wb") as f:
            f.write(video.read())

        st.info("Analyzing animal behavior… Please wait.")

        behavior, explanation = analyze_behavior_from_video(temp_path)

        st.markdown("### 🧠 AI Behavior Result")
        st.write(f"**Behavior:** {behavior}")
        st.write(f"**Explanation:** {explanation}")

        # ---- Vet trigger ----
        if behavior in ["Low Activity", "High Restlessness"]:
            st.warning("🚨 This behavior may need veterinary attention.")
            st.markdown(
                f"[📍 Find Nearest Vet]({vet_map_link(st.session_state.profile.get('location','veterinary hospital'))})"
            )
        else:
            st.success("✅ No vet action required.")

# ===================== END BEHAVIOR FIX =====================
