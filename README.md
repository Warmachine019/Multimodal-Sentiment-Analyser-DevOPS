# Multimodal Real-Time Emotion and Sentiment Detection System using Machine Learning

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=flat-square&logo=flask)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?style=flat-square&logo=opencv)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)

A real-time, zero-latency mental well-being monitoring dashboard that fuses visual, audio, and textual data to accurately detect human emotions. Built to compensate for the environmental vulnerabilities of unimodal systems (like bad lighting or background noise) using a custom **Late-Fusion Probability Weighting** algorithm.

**Developed by:** Spandan Sahai & Kaustav Roy

---

##  Key Features

* **Facial Emotion Recognition (FER):** Continuous, real-time bounding-box tracking using OpenCV and a CNN-based FER model.
* **Live Dictation & Audio Sentiment:** Bypasses traditional acoustic noise issues by utilizing dynamic Speech-to-Text (STT) transcription paired with deep learning NLP.
* **Manual Context Input:** Allows users to manually type their feelings for baseline emotional mapping.
* **Late-Fusion Algorithm:** Dynamically calculates confidence weights from all three modalities to output a single, highly accurate emotion (Happy, Sad, Neutral) and a `0-100` Happiness Score.
* **Zero-Latency Multithreading:** Hardware components (Webcam & Mic) run on decoupled background Python daemon threads, preventing UI freezing and ensuring smooth 1000ms polling.
* **Glassmorphism UI:** A sleek, modern dark-mode dashboard with dynamic color-shifting and animated progress bars.

---

##  Technology Stack

* **Backend:** Python, Flask, `threading`
* **Computer Vision:** OpenCV, `fer` (Facial Expression Recognition)
* **Audio Processing:** `SpeechRecognition`, PyAudio (Google STT API)
* **Natural Language Processing (NLP):** HuggingFace `transformers` (Sentiment-Analysis Pipeline)
* **Frontend:** HTML5, CSS3, Vanilla JavaScript (Asynchronous Fetch API)

---

##  Project Structure

```text
multimodal_emotion_system/
│
├── app.py                  # Main Flask application and API routes
├── static/                 
│   └── styles.css          # Glassmorphism UI styling and animations
├── templates/
│   └── index.html          # Web dashboard structure and JS polling logic
│
├── face/
│   ├── __init__.py
│   └── predict.py          # OpenCV continuous webcam feed & FER inference
│
├── speech/
│   ├── __init__.py
│   └── predict.py          # Background ambient listening & STT transcription
│
├── text/
│   ├── __init__.py
│   └── predict.py          # HuggingFace Transformer initialization & mapping
│
└── fusion/
    ├── __init__.py
    └── late_fusion.py      # Confidence calculation & score aggregation logic
