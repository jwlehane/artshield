from fastapi import APIRouter, UploadFile, File, Response
from PIL import Image, ImageDraw, ImageFont
import io

router = APIRouter(prefix="/api/protect", tags=["protection"])

@router.post("/strip-metadata")
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
