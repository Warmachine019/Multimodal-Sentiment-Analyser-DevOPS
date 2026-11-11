# face/predict.py  (cloud version: analyses a frame sent by the browser, no server webcam)
import base64
import threading

import cv2
import numpy as np
from fer.fer import FER

detector = FER()
_lock = threading.Lock()  # the Keras model is not safe to call from several threads at once

DEFAULT = {"happy": 0.0, "sad": 0.0, "neutral": 1.0}


def analyze_frame(data_url):
    """Takes a base64 JPEG (data URL or raw base64). Returns (emotion_dict, box_or_None)."""
    if not data_url:
        return dict(DEFAULT), None
    try:
        raw = base64.b64decode(data_url.split(",", 1)[-1])
        img = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return dict(DEFAULT), None
        with _lock:
            result = detector.detect_emotions(img)
    except Exception:
        return dict(DEFAULT), None

    if not result:
        return dict(DEFAULT), None

    emotions = result[0]["emotions"]
    x, y, w, h = [int(v) for v in result[0]["box"]]

    # same grouping as the original code
    happy = emotions["happy"]
    sad = emotions["sad"] + emotions["fear"] + emotions["angry"]
    neutral = emotions["neutral"] + emotions["surprise"] + emotions["disgust"]
    total = happy + sad + neutral
    if total <= 0:
        return dict(DEFAULT), {"x": x, "y": y, "w": w, "h": h}

    return (
        {"happy": happy / total, "sad": sad / total, "neutral": neutral / total},
        {"x": x, "y": y, "w": w, "h": h},
    )
