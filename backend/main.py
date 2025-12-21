from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
import uuid
import json
from concurrent.futures import ProcessPoolExecutor
import asyncio
from processor import ImageProcessor, ProtectionParams, ProtectionType, Intensity, ProtectionResult
from typing import Dict, Any
from multiprocessing import Manager
from contextlib import asynccontextmanager

# Global task proxy (will be initialized in lifespan)
tasks = None
process_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global tasks, process_pool
    # Initialize shared memory manager and process pool
    with Manager() as manager:
        tasks = manager.dict()
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as pool:
            process_pool = pool
            yield
            # Cleanup happen automatically when exiting the with-blocks
            # But the yield finishes when the app stops.

app = FastAPI(title="ArtShield API (Agent 2)", version="1.0", lifespan=lifespan)

# Setup directories
UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

# CORS for local development
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3333",
    "http://127.0.0.1:3333",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount processed images for static access
app.mount("/processed", StaticFiles(directory=PROCESSED_DIR), name="processed")

# Process Pool for CPU-bound image tasks
# process_pool = ProcessPoolExecutor() # Moved to lifespan

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "ArtShield Backend (Agent 2) is running"}

def run_pipeline(task_id: str, params: ProtectionParams, tasks_proxy: Dict[str, Any]):
    """
    Function to run in a separate process.
    """
    try:
        # We must update the proxy dict by re-assigning or using a nested structure carefully.
        # Simple approach: get the task, update it, put it back.
        task = tasks_proxy[task_id]
        task["status"] = "processing"
        task["progress"] = 10
        task["message"] = "Initializing engine..."
        tasks_proxy[task_id] = task

        processor = ImageProcessor(params.image_path)
        
        task = tasks_proxy[task_id]
        task["progress"] = 30
        task["message"] = "Applying adversarial protection..."
        tasks_proxy[task_id] = task
        
        result = processor.process(params)
        
        task = tasks_proxy[task_id]
        if not result.success:
            task["status"] = "failed"
            task["error"] = result.error
            task["message"] = f"Error: {result.error}"
            tasks_proxy[task_id] = task
            return task_id

        task["status"] = "completed"
        task["progress"] = 100
        task["message"] = "Protection applied successfully"
        task["processed_url"] = f"http://localhost:8999/processed/{os.path.basename(result.protected_path)}"
        tasks_proxy[task_id] = task
        return task_id
    except Exception as e:
        task = tasks_proxy[task_id]
        task["status"] = "failed"
        task["error"] = str(e)
        task["message"] = f"System Error: {str(e)}"
        tasks_proxy[task_id] = task
        return task_id

@app.get("/api/status/{task_id}")
async def get_task_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/api/process")
async def process_image(
    file: UploadFile = File(...),
    protection_type: str = Form("cloak_and_tag"),
    intensity: str = Form("medium"),
    metadata: str = Form("{}")
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    task_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]
    input_filename = f"{task_id}{extension}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)
    
    output_filename = f"{task_id}_processed{extension}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)

    # Initialize task state
    tasks[task_id] = {
        "id": task_id,
        "status": "pending",
        "progress": 0,
        "message": "Upload complete, queueing task...",
        "original_filename": file.filename
    }

    try:
        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse metadata JSON
        try:
            metadata_dict = json.loads(metadata)
        except json.JSONDecodeError:
            metadata_dict = {}
            
        # Create ProtectionParams
        params = ProtectionParams(
            image_path=input_path,
            output_path=output_path,
            protection_type=ProtectionType(protection_type),
            intensity=Intensity(intensity),
            metadata=metadata_dict
        )
            
        # Run processing in background process - NON-BLOCKING
        loop = asyncio.get_event_loop()
        # Pass the global tasks proxy to the executor
        loop.run_in_executor(process_pool, run_pipeline, task_id, params, tasks)
        
        return {
            "status": "accepted",
            "task_id": task_id
        }

    except Exception as e:
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error"] = str(e)
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8999, reload=True)
