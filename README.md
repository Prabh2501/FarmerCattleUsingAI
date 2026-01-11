**Smart Farm OS** is an AI-assisted livestock monitoring system designed to **reduce the daily decision burden on farmers**, especially small and resource-constrained ones.

The system uses **computer vision and lightweight AI** to:

* Automatically detect animals from images, videos, and live camera feeds
* Track attendance without manual input
* Provide **early health and behavior warnings**
* Suggest veterinary support when required

> ⚠️ **Important Philosophy**
> AI in this system **does not replace farmers or veterinarians**.
> It **supports** decision-making by reducing repetitive work and highlighting risks early.

---

## 🎯 Problem We Address

* Manual livestock monitoring is time-consuming and error-prone
* Health issues are often detected **too late**
* Farmers are overloaded with small, repetitive decisions
* Most AI solutions are expensive, complex, or require constant maintenance

Smart Farm OS focuses on **simplicity, transparency, and accessibility**.

---

## ✨ Key Features

### 🐄 Animal Detection

* Image upload detection
* Video-based detection
* Live camera (webcam) detection
* Multi-animal detection in a single frame
* Automatic animal type identification (no manual input)

---

### 📊 Automatic Attendance

* Unique ID generated per animal using visual hashing
* Same animal re-appearing → **attendance not duplicated**
* Fully automatic (no “register attendance” button)

---

### 🩺 Health Monitoring

* Confidence-based health estimation
* Clear farmer-friendly statuses:

  * **Healthy**
  * **Needs Vet Support**
* No complex medical terms exposed

---

### 🧠 Behavioral Analysis (Video)

* Motion-based behavior assessment
* Detects:

  * Low activity (possible weakness)
  * High restlessness (possible stress or pain)
  * Normal behavior
* Always provides **explainable output**

---

### 🩺 Conditional Vet Support

* Vet recommendations shown **only when required**
* Google Maps integration for nearest veterinary services
* Avoids unnecessary alerts

---

### 👨‍🌾 Farmer-Friendly Dashboard

* Card view and table view toggle
* Animal emojis for quick recognition
* Editable animal names
* One-click record deletion
* No backend IDs shown to farmers

---

### 🌐 Language Support

* English
* Hindi (expandable)

---

### 📴 Offline-Friendly Design

* Runs fully on local machine
* CSV-based storage
* No mandatory cloud or internet dependency
* Designed for rural and low-connectivity environments

---

## 🧱 System Architecture

```
User (Farmer)
   │
   ▼
Streamlit UI (White + Green, Card-Based)
   │
   ▼
AI Layer (YOLOv8 - CPU Friendly)
   │
   ▼
Behavior & Health Logic (Explainable Rules)
   │
   ▼
Local Backend (CSV Database)
```

---

## 🧠 AI Models Used

### YOLOv8 Nano (`yolov8n`)

* Real-time object detection
* Lightweight and CPU-friendly
* Pretrained on COCO dataset
* Suitable for low-resource systems

> No retraining required for MVP.

---

## ⚙️ Tech Stack

| Component       | Technology               |
| --------------- | ------------------------ |
| Frontend        | Streamlit                |
| AI Model        | YOLOv8 (Ultralytics)     |
| Computer Vision | OpenCV                   |
| Backend         | Python + Pandas          |
| Storage         | CSV (Offline First)      |
| Mapping         | Google Maps (link-based) |

---

## 🗂️ Project Structure

```
livestock_final/
│
├── app.py
├── yolov8n.pt
├── records.csv
│
├── backend/
│   └── database.py
│
└── ui/
    ├── styles.py
    ├── sidebar.py
    ├── header.py
    └── dashboard.py
```

---

## ▶️ How to Run

### 1️⃣ Install dependencies

```bash
pip install streamlit ultralytics opencv-python pandas numpy
```

### 2️⃣ Place YOLO model

Download `yolov8n.pt` and place it in the project root.

### 3️⃣ Run the app

```bash
streamlit run app.py
```

---

## 🔐 Ethical & Design Considerations

* AI outputs are **advisory**, not authoritative
* No medical diagnosis claims
* Farmer and veterinarian retain final control
* Transparent explanations provided for every AI suggestion

---

## 🚀 Future Scope

* Individual animal behavior history
* Disease-specific ML models
* Mobile app interface
* Cloud sync for large farms
* Government database integration (ear tags / RFID)
* Multi-language expansion

---

## 🏁 Conclusion

Smart Farm OS demonstrates how **practical, explainable AI** can support farmers without increasing complexity or cost.

It is:

* Technically feasible
* Ethically sound
* Scalable
* Farmer-centric

---

## 👥 Team

**Project Type:** Prototype / Hackathon MVP
**Domain:** AI for Agriculture
Working site: https://smartfarm-oc84.onrender.com/
