from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
import os
import asyncio
import uuid
from typing import List, Dict

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

# In-memory storage for task status
tasks: Dict[str, dict] = {}

class TaskResponse(BaseModel):
    id: str

class StatusResponse(BaseModel):
    id: str
    status: str
    progress: int
    message: str

async def simulate_processing(task_id: str):
    """Simulates the image processing pipeline."""
    try:
        tasks[task_id]["status"] = "processing"
        tasks[task_id]["progress"] = 0
        tasks[task_id]["message"] = "Initializing..."
        await asyncio.sleep(1)

        # Step 1: Mist Cloak
        tasks[task_id]["message"] = "Applying Mist Cloak..."
        for i in range(10, 50, 10):
            tasks[task_id]["progress"] = i
            await asyncio.sleep(0.5)

        # Step 2: Metadata
        tasks[task_id]["message"] = "Injecting Metadata..."
        for i in range(50, 80, 10):
            tasks[task_id]["progress"] = i
            await asyncio.sleep(0.5)

        # Step 3: Watermark
        tasks[task_id]["message"] = "Finalizing Watermark..."
        for i in range(80, 100, 10):
            tasks[task_id]["progress"] = i
            await asyncio.sleep(0.5)

        tasks[task_id]["progress"] = 100
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["message"] = "Protection Complete"

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["message"] = f"Error: {str(e)}"

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "ArtShield Backend is running"}

@app.post("/api/process", response_model=TaskResponse)
async def process_endpoint(files: List[UploadFile] = File(...), background_tasks: BackgroundTasks = None):
    # Generate a unique ID for this processing task
    task_id = str(uuid.uuid4())

    # Initialize task status
    tasks[task_id] = {
        "id": task_id,
        "status": "pending",
        "progress": 0,
        "message": "Queued"
    }

    # Start background processing
    if background_tasks is not None:
        background_tasks.add_task(simulate_processing, task_id)
    else:
        # Fallback if somehow background_tasks is not injected, though it should be
        asyncio.create_task(simulate_processing(task_id))

    return {"id": task_id}

@app.get("/api/status/{task_id}", response_model=StatusResponse)
async def get_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

# In production, we will mount the frontend build directory here
# if os.path.exists("static"):
#    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8999, reload=True)
