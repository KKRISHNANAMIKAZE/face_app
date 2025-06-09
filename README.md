# Face Recognition & RAG Chatbot Platform

A smart web application that allows users to register and recognize faces using 128-dimensional facial encodings and interact with a chatbot powered by Retrieval-Augmented Generation (RAG). The project includes live face registration and recognition, as well as the ability to ask questions about recent activity.

## 🔧 Features
- Register faces with names using a webcam image.
- Real-time face recognition with bounding boxes.
- Stores 128-d facial encodings and metadata (name and timestamp) in a JSON file or Firebase.
- Chatbot interface powered by LangChain, FAISS, and LLaMA3/OpenAI API.
- Logs maintained for registration, recognition, and chat for tracking events.
- Organized frontend UI with React and backend logic using FastAPI (Python) and Node.js.

## 🧠 Technologies Used
- **ML**: `face_recognition` for generating 128-d vector encodings.
- **Chat AI**: LangChain, FAISS, LLaMA3/OpenAI.
- **Frontend (React)**:
  - `App.jsx`: Entry point for the app.
  - `RegistrationFace.jsx`: Handles face registration UI.
  - `RecognizeFace.jsx`: Manages webcam-based live recognition.
  - `ChatInterface.jsx`: Provides chatbot interface.
- **Backend**:
  - `face_system.py` (FastAPI): Processes registration, recognition, chat, and memory.
  - `Node.js server`: Handles image upload endpoints.
- **Database**: JSON file and Firebase (optional).
- **Logging**: Events logged to `registration.log`, `recognition.log`, and `chat.log`.

## 🚀 Setup
```bash
# Frontend
cd frontend
npm install
npm run dev

# Python backend
cd face
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn face_system:app --reload --port 5000

# Node backend
cd node-backend
npm install
node index.js
ARCHITECTURE DIAGRAM :
+--------------------+          +-------------------+          +-------------------+
|                    |          |                   |          |                   |
|    React Frontend   | <------> |   Node.js Server  | <------> |   Firebase/JSON   |
|  (Registration,     |  REST/  | (Image Upload     |  Stores | (Facial Data and  |
|   Recognition, Chat)|  HTTP   |  Endpoints)       |  Data   |  Metadata Storage)|
|                    |          |                   |          |                   |
+--------------------+          +-------------------+          +-------------------+
         |                                   ^
         |                                   |
         |                                   |
         v                                   |
+--------------------+                      |
|                    |                      |
|   FastAPI Backend   | <-------------------+
| (Face Recognition,  |
|  Embedding, Chatbot)|
|                    |
+--------------------+

demo link : 
This project is a part of a hackathon run by https://katomaran.com
