# fusion/late_fusion.py

def fuse(face, text, speech):
    face = face or {}
    text = text or {}
    speech = speech or {}

    face_conf = max(face.values()) if face else 0.0
    text_conf = max(text.values()) if text else 0.0
    speech_conf = max(speech.values()) if speech else 0.0

    total = face_conf + text_conf + speech_conf

    if total > 0:
        w_face = face_conf / total
        w_text = text_conf / total
        w_speech = speech_conf / total
    else:
        w_face = 1.0 / 3.0
        w_text = 1.0 / 3.0
        w_speech = 1.0 / 3.0

    final = {}
    for emotion in ["happy", "sad", "neutral"]:
        final[emotion] = (
            w_face * face.get(emotion, 0.0) +
            w_text * text.get(emotion, 0.0) +
            w_speech * speech.get(emotion, 0.0)
        )

    final_emotion = max(final, key=final.get) if final else "neutral"

    # Calculate 0-100 Happiness Score
    happiness_score = (final.get("happy", 0.0) * 100) + (final.get("neutral", 0.0) * 50) + (final.get("sad", 0.0) * 0)

    return final, final_emotion, w_face, w_text, w_speech, happiness_score
