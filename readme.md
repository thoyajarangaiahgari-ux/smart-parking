# 🅿️ ParkSmart: Next-Generation Intelligent Mobility & Accessibility Core

ParkSmart is a premium, enterprise-grade edge computer vision solution engineered to optimize urban parking logistics, minimize transit idle times, and reduce vehicular emissions. Powered by a custom deep learning Convolutional Neural Network (CNN), the platform performs real-time occupancy audits on parking lot matrices.

To bridge the gap between high-level artificial intelligence and diverse real-world users, ParkSmart features a fluidly localized dashboard and a dynamic, in-memory Text-to-Speech (TTS) announcement layer supporting 5 major regional languages.

---

## 🚀 Key Presentation Highlights

* **Automated CNN Inference Core:** Real-time spot classification using a pre-trained Keras/TensorFlow model (`new_smart_parking_cnn.h5`) that automatically scales matrix resolutions without dimension conflicts.
* **Instant dedicated Viewport Shift:** The moment an operator uploads an image feed, the interface seamlessly re-renders to focus entirely on the AI inference output at the top of the viewport—eliminating any manual scrolling.
* **Holographic Branding & UI Elements:** Replaces basic standby boxes with a custom vector branding emblem displaying a high-contrast futuristic parking layout and a personalized localized user greeting card.
* **Globalized Audio Localization Engine:** True system-wide translations and automated voice announcements mapped for **English, Telugu (తెలుగు), Tamil (தமிழ்), Malayalam (മലയാളം), and Hindi (हिन्दी)**.
* **Hardware-Accelerated Fluid Aesthetics:** Immersive background featuring fully offline, CSS-driven holographic vehicles (cars 🚗 and motorcycles 🏍) drifting dynamically across the stage with glow paths.

---

## 🛠️ System Architecture & Tech Stack

* **Pipeline Language Core:** Python 3.10+
* **Deep Learning Framework:** TensorFlow / Keras 2.x+
* **Front-End Orchestration:** Streamlit Server Node
* **Speech Synthesis Engine:** Google Text-To-Speech (gTTS) Native Wrapper
* **Image Processing Pipelines:** Pillow (PIL) & NumPy Matrix Vectors
* **Aesthetics Engine:** Hardware-Accelerated CSS / Inline HTML SVGs

---

## 📂 Project Workspace Structure

Your workspace directory on the local `D:` drive is cleanly structured as follows:

```text
D:\website\
│
├── new_smart_parking_cnn.h5    # Pre-trained Deep Learning CNN model weights
├── app.py                      # Core web dashboard application & multi-lingual logic
├── requirements.txt            # Project dependencies manifest file
└── README.md                   # Comprehensive presentation documentation (This file)