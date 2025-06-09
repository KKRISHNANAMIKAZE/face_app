from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import face_recognition
import numpy as np
import json
import cv2

app = FastAPI()

# Enable CORS for all origins (change "*" if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "backend/db.json"

# Load known face data (encoding stored as list, convert to numpy array)
with open(DB_PATH, "r") as f:
    data = json.load(f)

known_encodings = [np.array(entry["encoding"]) for entry in data]
known_names = [entry["name"] for entry in data]


@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    results = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            index = matches.index(True)
            name = known_names[index]
        results.append({"name": name})

    return {"faces": results}


def generate_frames():
    video = cv2.VideoCapture(0)  # Use your webcam
    if not video.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        success, frame = video.read()
        if not success:
            break

        # Optionally do recognition here if needed — currently just streaming raw frames

        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()

        # Yield frame bytes in multipart format for MJPEG streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    video.release()


@app.get("/live-feed")
def live_feed():
    return StreamingResponse(generate_frames(),
                             media_type='multipart/x-mixed-replace; boundary=frame')
