# test_face.py
from face.predict import get_face_data
import time

print("Starting camera... Please smile!")
time.sleep(3) # wait for camera to warm up

while True:
    emotion_dict, _ = get_face_data()
    print(f"Face Only Probabilities: {emotion_dict}")
    time.sleep(1)