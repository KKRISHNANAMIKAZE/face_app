from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.middleware.cors import CORSMiddleware
import face_recognition
import numpy as np
import cv2
from datetime import datetime
from langchain.docstore.document import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA
import firebase_admin
from firebase_admin import credentials, firestore

# ----------------- Initialize App -----------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Firebase Setup -----------------
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
collection_name = "face_encodings"

# ----------------- Global Memory -----------------
last_registered = {"name": None, "timestamp": None}

# ----------------- Register Face -----------------
@app.post("/register-face")
async def register_face(name: str = Form(...), file: UploadFile = File(...)):
    image_data = await file.read()
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

    face_locations = face_recognition.face_locations(image)
    if not face_locations:
        return {"status": "error", "message": "No face detected"}

    face_encoding = face_recognition.face_encodings(image, face_locations)[0].tolist()
    timestamp = datetime.now().isoformat()

    doc_ref = db.collection(collection_name).document()
    doc_ref.set({
        "name": name,
        "encoding": face_encoding,
        "timestamp": timestamp
    })

    last_registered["name"] = name
    last_registered["timestamp"] = timestamp

    return {"status": "success", "message": f"{name} registered successfully"}

# ----------------- Recognize Face -----------------
@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    docs = db.collection(collection_name).stream()
    known_encodings = []
    known_names = []
    for doc in docs:
        data = doc.to_dict()
        known_encodings.append(np.array(data["encoding"]))
        known_names.append(data["name"])

    results = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"
        if True in matches:
            index = matches.index(True)
            name = known_names[index]

        results.append({
            "name": name,
            "top": top * 4,
            "right": right * 4,
            "bottom": bottom * 4,
            "left": left * 4
        })

    return {"faces": results}

# ----------------- Chat RAG -----------------
@app.post("/chat")
async def chat_query(request: Request):
    question = (await request.json()).get("query", "")
    if not question:
        return {"error": "No query provided"}

    docs_snapshot = db.collection(collection_name).stream()
    docs = []
    for doc in docs_snapshot:
        d = doc.to_dict()
        docs.append(Document(
            page_content=f"{d['name']} was registered at {d['timestamp']}",
            metadata=d
        ))

    embedding = OllamaEmbeddings(model="llama3")
    vectorstore = FAISS.from_documents(docs, embedding)
    llm = ChatOllama(model="llama3")
    qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

    answer = qa.run(question)
    return {"response": answer}

# ----------------- Last Registered Memory -----------------
@app.get("/last-registered")
async def get_last_registered():
    return last_registered if last_registered["name"] else {"message": "No one registered yet."}
