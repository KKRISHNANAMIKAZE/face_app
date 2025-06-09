from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
from langchain.docstore.document import Document
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from langchain.chains import RetrievalQA

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "backend/db.json"

# Load data and prepare RAG pipeline
with open(DB_PATH, "r") as f:
    db = json.load(f)

docs = [Document(page_content=f"{entry['name']} was registered at {entry['timestamp']}.", metadata=entry) for entry in db]

embedding = OllamaEmbeddings(model="llama3")
vectorstore = FAISS.from_documents(docs, embedding)
llm = ChatOllama(model="llama3")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())

@app.post("/chat")
async def chat_query(request: Request):
    body = await request.json()
    question = body.get("query", "")

    if not question:
        return {"error": "No query provided"}

    answer = qa.run(question)
    return {"response": answer}
