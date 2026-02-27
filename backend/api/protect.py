from fastapi import APIRouter, UploadFile, File, Response, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from PIL import Image, ImageDraw, ImageFont
import io
import uuid
import os
import shutil
from typing import List

try:
    from backend.database import get_db, ProtectedAsset
except ImportError:
    from database import get_db, ProtectedAsset

router = APIRouter(prefix="/api", tags=["protection"])

UPLOAD_DIR = "data/uploads"
SHIELDED_DIR = "data/shielded"

# Ensure directories exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(SHIELDED_DIR, exist_ok=True)

def strip_metadata_logic(image: Image.Image) -> io.BytesIO:
    output = io.BytesIO()
    image.save(output, format=image.format)
    output.seek(0)
    return output

def watermark_logic(original_image: Image.Image) -> io.BytesIO:
    format = original_image.format
    image = original_image.convert("RGBA")
    
    # Create watermark layer
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    
    # Simple watermark text at the bottom right
    width, height = image.size
    text = "ArtShield Protected"
    
    # We'll use a default font
    draw.text((width - 150, height - 30), text, fill=(255, 255, 255, 128))
    
    combined = Image.alpha_composite(image, txt)
    
    output = io.BytesIO()
    # Convert back to RGB to save as JPEG if needed
    if format == "JPEG":
        combined = combined.convert("RGB")
    
    combined.save(output, format=format or "PNG")
    output.seek(0)
    return output

async def process_task_assets(task_id: str, db: Session):
    assets = db.query(ProtectedAsset).filter(ProtectedAsset.task_id == task_id).all()
    
    for asset in assets:
        try:
            asset.status = "processing"
            db.commit()
            
            # 1. Strip Metadata
            with Image.open(asset.original_path) as img:
                # We do both: strip metadata and watermark
                # First, get the format
                fmt = img.format
                
                # Apply watermark (this also effectively strips metadata by creating a new image)
                watermarked_io = watermark_logic(img)
                
                # Save to shielded path
                shielded_filename = f"shielded_{os.path.basename(asset.original_path)}"
                shielded_path = os.path.join(SHIELDED_DIR, shielded_filename)
                
                with open(shielded_path, "wb") as f:
                    f.write(watermarked_io.getvalue())
                
                asset.shielded_path = shielded_path
                asset.status = "completed"
                db.commit()
        except Exception as e:
            print(f"Error processing asset {asset.id}: {e}")
            asset.status = "failed"
            db.commit()

@router.post("/process")
async def process_images(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    task_id = str(uuid.uuid4())
    
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, f"{task_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        new_asset = ProtectedAsset(
            task_id=task_id,
            original_name=file.filename,
            original_path=file_path,
            status="pending"
        )
        db.add(new_asset)
    
    db.commit()
    
    background_tasks.add_task(process_task_assets, task_id, db)
    
    return {"id": task_id, "status": "accepted"}

@router.get("/status/{task_id}")
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    assets = db.query(ProtectedAsset).filter(ProtectedAsset.task_id == task_id).all()
    if not assets:
        raise HTTPException(status_code=404, detail="Task not found")
    
    completed = sum(1 for a in assets if a.status == "completed")
    failed = sum(1 for a in assets if a.status == "failed")
    total = len(assets)
    
    # Calculate progress
    progress = 0
    if total > 0:
        progress = int(((completed + failed) / total) * 100)
    
    # Determine overall status
    if failed > 0 and (completed + failed) == total:
        status = "failed"
    elif completed == total:
        status = "completed"
    elif any(a.status == "processing" for a in assets):
        status = "processing"
    else:
        status = "pending"
        
    return {
        "id": task_id,
        "status": status,
        "progress": progress,
        "message": f"Processed {completed}/{total} assets"
    }

@router.post("/protect/strip-metadata")
async def strip_metadata(file: UploadFile = File(...)):
    """
    Strips all EXIF and other metadata from the uploaded image.
    Returns the image without metadata.
    """
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    
    # Strip metadata by saving without EXIF
    output = io.BytesIO()
    image.save(output, format=image.format)
    output.seek(0)
    
    return Response(content=output.getvalue(), media_type=f"image/{image.format.lower()}")

@router.post("/watermark")
async def watermark(file: UploadFile = File(...)):
    """
    Applies a simple 'ArtShield Protected' watermark to the bottom right of the image.
    Returns the watermarked image.
    """
    contents = await file.read()
    original_image = Image.open(io.BytesIO(contents))
    format = original_image.format
    image = original_image.convert("RGBA")
    
    # Create watermark layer
    txt = Image.new("RGBA", image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt)
    
    # Simple watermark text at the bottom right
    width, height = image.size
    text = "ArtShield Protected"
    
    # We'll use a default font
    draw.text((width - 150, height - 30), text, fill=(255, 255, 255, 128))
    
    combined = Image.alpha_composite(image, txt)
    
    output = io.BytesIO()
    # Convert back to RGB to save as JPEG if needed
    if format == "JPEG":
        combined = combined.convert("RGB")
    
    combined.save(output, format=format or "PNG")
    output.seek(0)
    
    return Response(content=output.getvalue(), media_type=f"image/{(format or 'PNG').lower()}")
