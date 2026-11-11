# speech/predict.py  (cloud version: speech-to-text now happens in the browser (Web Speech API);
# the server only turns the transcript into an emotion using the existing text model)
from text.predict import get_text_emotion

DEFAULT = {"happy": 0.0, "sad": 0.0, "neutral": 1.0}


def analyze_speech(transcript):
    transcript = (transcript or "").strip()
    if not transcript:
        return dict(DEFAULT), "Speak into your microphone...", "Listening..."
    return get_text_emotion(transcript), transcript, "Done"
