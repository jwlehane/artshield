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
from processor import ImageProcessor, ProtectionParams, ProtectionType, Intensity

app = FastAPI(title="ArtShield API (Agent 2)", version="1.0")

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
process_pool = ProcessPoolExecutor()

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "ArtShield Backend (Agent 2) is running"}

def run_pipeline(params: ProtectionParams):
    """
    Function to run in a separate process.
    """
    processor = ImageProcessor(params.image_path)
    # The unified process method handles Cloak, Poison, and Tag
    result = processor.process(params)
    if not result.success:
        raise Exception(result.error)
    return result.protected_path

@app.post("/api/process")
async def process_image(
    file: UploadFile = File(...),
    protection_type: str = Form("cloak_and_tag"),
    intensity: str = Form("medium"),
    metadata: str = Form("{}")
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    file_id = str(uuid.uuid4())
    extension = os.path.splitext(file.filename)[1]
    input_filename = f"{file_id}{extension}"
    input_path = os.path.join(UPLOAD_DIR, input_filename)
    
    output_filename = f"{file_id}_processed{extension}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)

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
            
        # Run processing in background process
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(process_pool, run_pipeline, params)
        
        # Return URL to processed image
        # Assuming server runs on localhost:8999 for now as per plan
        processed_url = f"http://localhost:8999/processed/{output_filename}"
        
        return {
            "status": "success",
            "original_filename": file.filename,
            "processed_url": processed_url
        }

    except Exception as e:
        # Clean up if possible
        if os.path.exists(input_path):
            os.remove(input_path)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8999, reload=True)
