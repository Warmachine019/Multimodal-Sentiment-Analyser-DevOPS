# text/predict.py
from transformers import pipeline

# Load once (important)
classifier = pipeline("sentiment-analysis")


def get_text_emotion(text):
    if not text or not str(text).strip():
        # Fallback if no text is provided
        return {"happy": 0.0, "sad": 0.0, "neutral": 1.0}

    cleaned_text = str(text).strip()
    result = classifier(cleaned_text, truncation=True, max_length=512)[0]
    label = result["label"]
    score = float(result["score"])

    if label == "POSITIVE":
        return {
            "happy": score,
            "sad": 0.0,
            "neutral": max(0.0, 1.0 - score)
        }
    else:
        return {
            "happy": 0.0,
            "sad": score,
            "neutral": max(0.0, 1.0 - score)
        }
