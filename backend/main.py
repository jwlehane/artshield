from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

try:
    from backend.api import protect
    from backend.database import init_db
except ImportError:
    from api import protect
    from database import init_db

app = FastAPI(title="ArtShield API", version="1.0")

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(protect.router)

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
    import uvicorn
    # Use the app object directly to avoid import issues with uvicorn.run string reference
    uvicorn.run(app, host="127.0.0.1", port=8999)
