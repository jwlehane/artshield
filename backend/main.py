from fastapi import FastAPI, BackgroundTasks, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import uuid
import asyncio
from typing import List, Dict, Any

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

# In-memory storage for tasks
TASKS: Dict[str, Dict[str, Any]] = {}

async def process_task(task_id: str):
    """
    Simulates a long-running image processing task.
    """
    try:
        TASKS[task_id].update({
            "status": "processing",
            "progress": 0,
            "message": "Initializing..."
        })

        # Step 1: Mist Cloak
        await asyncio.sleep(1.5)
        TASKS[task_id].update({
            "progress": 30,
            "message": "Applying Mist Cloak..."
        })

        # Step 2: Metadata
        await asyncio.sleep(1.5)
        TASKS[task_id].update({
            "progress": 60,
            "message": "Injecting Metadata..."
        })

        # Step 3: Finalizing
        await asyncio.sleep(1.0)
        TASKS[task_id].update({
            "progress": 90,
            "message": "Finalizing Watermark..."
        })

        # Complete
        await asyncio.sleep(0.5)
        TASKS[task_id].update({
            "status": "completed",
            "progress": 100,
            "message": "Protection Complete"
        })

    except Exception as e:
        print(f"Error processing task {task_id}: {e}")
        TASKS[task_id].update({
            "status": "failed",
            "message": "Processing failed"
        })

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "ArtShield Backend is running"}

@app.post("/api/process")
async def process_images(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    task_id = str(uuid.uuid4())
    TASKS[task_id] = {
        "id": task_id,
        "status": "pending",
        "progress": 0,
        "message": "Queued"
    }

    background_tasks.add_task(process_task, task_id)

    return {"id": task_id}

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    if task_id not in TASKS:
        raise HTTPException(status_code=404, detail="Task not found")
    return TASKS[task_id]

# In production, we will mount the frontend build directory here
# if os.path.exists("static"):
#    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8999, reload=True)
