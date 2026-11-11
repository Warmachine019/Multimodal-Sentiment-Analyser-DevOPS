# app.py  (cloud version: the BROWSER captures camera + mic, the server only runs the models)
import json
import logging
import os
import time

from flask import Flask, render_template, request, jsonify, Response
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

from face.predict import analyze_frame
from text.predict import get_text_emotion
from speech.predict import analyze_speech
from fusion.late_fusion import fuse
from storage import record_result

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("sentiment")

app = Flask(__name__)

# ---- Prometheus metrics (scraped from /metrics) ----
ANALYSES = Counter("sentiment_analyses", "Number of analyses, by final fused emotion", ["emotion"])
NO_FACE = Counter("sentiment_no_face", "Requests where no face was detected")
HAPPINESS = Gauge("sentiment_happiness_score", "Most recent happiness score (0-100)")
REQ_SECONDS = Histogram("sentiment_request_seconds", "Total time of one /analyze request")
MODEL_SECONDS = Histogram("sentiment_model_seconds", "Time spent in each model", ["model"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route("/analyze", methods=["POST"])
def analyze():
    t_start = time.time()
    data = request.get_json(silent=True) or {}
    user_text = data.get("text", "")

    t = time.time()
    face_pred, face_box = analyze_frame(data.get("frame"))          # frame = base64 JPEG from browser
    MODEL_SECONDS.labels("face").observe(time.time() - t)
    if data.get("frame") and face_box is None:
        NO_FACE.inc()

    t = time.time()
    text_pred = get_text_emotion(user_text)
    MODEL_SECONDS.labels("text").observe(time.time() - t)

    t = time.time()
    speech_pred, speech_transcript, speech_status = analyze_speech(data.get("speech", ""))  # transcript from browser
    MODEL_SECONDS.labels("speech").observe(time.time() - t)

    fused_scores, final_emotion, w_face, w_text, w_speech, score = fuse(face_pred, text_pred, speech_pred)

    result = {
        "final_emotion": final_emotion,
        "happiness_score": round(score),
        "speech_transcript": speech_transcript,
        "speech_status": speech_status,
        "weights": {
            "face": round(w_face, 2),
            "text": round(w_text, 2),
            "speech": round(w_speech, 2),
        },
        "face": {"emotion": max(face_pred, key=face_pred.get), "box": face_box},
    }

    ANALYSES.labels(str(final_emotion)).inc()
    HAPPINESS.set(result["happiness_score"])
    REQ_SECONDS.observe(time.time() - t_start)

    log.info(json.dumps({"event": "analysis", "emotion": final_emotion,
                         "score": result["happiness_score"], "weights": result["weights"]}))
    record_result({"emotion": final_emotion, "score": result["happiness_score"], "weights": result["weights"]})

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
