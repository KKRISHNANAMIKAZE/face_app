from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import cv2
import numpy as np
import json
import os
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "backend/db.json"

# Create the db.json if it doesn't exist
if not os.path.exists(DB_PATH):
    with open(DB_PATH, "w") as f:
        json.dump([], f)

@app.post("/register-face")
async def register_face(name: str = Form(...), file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return {"status": "error", "message": "No face detected"}

    face_encoding = face_recognition.face_encodings(image, face_locations)[0]

    with open(DB_PATH, "r") as f:
        data = json.load(f)

    data.append({
        "name": name,
        "encoding": face_encoding.tolist(),
        "timestamp": datetime.now().isoformat()
    })

    with open(DB_PATH, "w") as f:
        json.dump(data, f)

    return {"status": "success", "message": f"{name} registered successfully"}
