from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Career Studio Backend API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from routers import router as knowledge_router

app.include_router(knowledge_router)
app.mount("/ui", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Career Studio AI Pipeline is running"}
