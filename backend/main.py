from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI(title="ArtShield API", version="1.0")

# CORS for local development (Vite runs on 5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "ArtShield Backend is running"}

# In production, we will mount the frontend build directory here
# if os.path.exists("static"):
#    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8999, reload=True)
