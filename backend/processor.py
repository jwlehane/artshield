from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import piexif
import os
import random
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, Dict

class ProtectionType(str, Enum):
    CLOAK = "cloak"
    TAG = "tag"
    CLOAK_AND_TAG = "cloak_and_tag"
    POISON = "poison"

class Intensity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ProtectionParams(BaseModel):
    image_path: str
    protection_type: ProtectionType = ProtectionType.CLOAK_AND_TAG
    intensity: Intensity = Intensity.MEDIUM
    output_path: Optional[str] = None
    metadata: Dict[str, str] = Field(default_factory=dict)

class ProtectionResult(BaseModel):
    success: bool
    original_path: str
    protected_path: Optional[str] = None
    message: Optional[str] = None
    error: Optional[str] = None

class HardwareInfo(BaseModel):
    device: str
    has_cuda: bool
    cuda_device_name: Optional[str] = None

class ImageProcessor:
    @staticmethod
    def get_hardware_info() -> HardwareInfo:
        """
        Detect local hardware capabilities (CPU vs GPU).
        """
        has_cuda = False
        device_name = None
        device = "cpu"
        
        try:
            import torch
            has_cuda = torch.cuda.is_available()
            if has_cuda:
                device = "cuda"
                device_name = torch.cuda.get_device_name(0)
        except ImportError:
            pass
            
        return HardwareInfo(
            device=device,
            has_cuda=has_cuda,
            cuda_device_name=device_name
        )

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.image = Image.open(file_path)
        # Ensure image is in RGB mode (handle RGBA or P)
        if self.image.mode != "RGB":
            self.image = self.image.convert("RGB")
        self.output_path = None
        self.exif_bytes = None

    def process(self, params: ProtectionParams) -> ProtectionResult:
        """
        Execute the protection pipeline based on params.
        """
        try:
            # 1. Apply Cloak (Glaze-style)
            if params.protection_type in [ProtectionType.CLOAK, ProtectionType.CLOAK_AND_TAG]:
                self.apply_cloak(params.intensity)
            
            # 2. Apply Poison (Nightshade-style)
            if params.protection_type == ProtectionType.POISON:
                self.apply_poison(params.intensity)

            # 3. Add Metadata (The Tag)
            if params.protection_type in [ProtectionType.TAG, ProtectionType.CLOAK_AND_TAG]:
                # Extract specific fields from metadata dict or use defaults
                author = params.metadata.get("author", "Unknown Artist")
                copyright_text = params.metadata.get("copyright", "Copyright 2025")
                noai = params.metadata.get("noai", "True")
                self.add_metadata(author, copyright_text, noai)

            # 4. Save
            if params.output_path:
                output_path = params.output_path
            else:
                # Generate default output path
                base, ext = os.path.splitext(self.file_path)
                output_path = f"{base}_protected.jpg"
            
            self.save(output_path)
            self.output_path = output_path
            
            return ProtectionResult(
                success=True,
                original_path=self.file_path,
                protected_path=output_path,
                message="Protection applied successfully"
            )

        except Exception as e:
            return ProtectionResult(
                success=False,
                original_path=self.file_path,
                error=str(e)
            )

    def resize(self, max_size: tuple[int, int]):
        """
        Resize image maintaining aspect ratio.
        max_size: (width, height)
        """
        self.image.thumbnail(max_size, Image.Resampling.LANCZOS)

    def apply_cloak(self, intensity: Intensity):
        """
        Apply adversarial noise (Glaze-style) to disrupt style mimicry.
        In this implementation, we add high-frequency, low-amplitude noise.
        """
        # Map intensity to noise level
        levels = {Intensity.LOW: 2, Intensity.MEDIUM: 5, Intensity.HIGH: 10}
        strength = levels.get(intensity, 5)

        # Implementation using PIL pixel access for wide compatibility
        pixels = self.image.load()
        width, height = self.image.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Add random noise
                dr = random.randint(-strength, strength)
                dg = random.randint(-strength, strength)
                db = random.randint(-strength, strength)
                pixels[x, y] = (
                    max(0, min(255, r + dr)),
                    max(0, min(255, g + dg)),
                    max(0, min(255, b + db))
                )
        
        print(f"Applied Cloak (Glaze-style) protection with {intensity} intensity")

    def apply_poison(self, intensity: Intensity):
        """
        Apply adversarial noise (Nightshade-style) to poison AI models.
        In this implementation, we apply a subtle color shift pattern.
        """
        levels = {Intensity.LOW: 1, Intensity.MEDIUM: 3, Intensity.HIGH: 5}
        strength = levels.get(intensity, 3)

        pixels = self.image.load()
        width, height = self.image.size
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Subtle shift based on position to create a 'pattern'
                shift = int(strength * ( (x % 10) - 5) / 5)
                pixels[x, y] = (
                    max(0, min(255, r + shift)),
                    max(0, min(255, g - shift)),
                    max(0, min(255, b + shift))
                )
        
        print(f"Applied Poison (Nightshade-style) protection with {intensity} intensity")

    def apply_mist(self):
        """
        Deprecated. Use apply_cloak or apply_poison.
        """
        self.apply_cloak(Intensity.MEDIUM)

    def apply_watermark(self, text: str):
        """
        Apply a visible watermark text to the image.
        """
        draw = ImageDraw.Draw(self.image)
        width, height = self.image.size
        
        # Try to load a default font, otherwise default to basic bitmap font
        try:
            # Arial for Windows, adjust for Linux/Mac if needed
            font = ImageFont.truetype("arial.ttf", size=int(height/20))
        except IOError:
            font = ImageFont.load_default()

        # Calculate text size using getbbox (left, top, right, bottom)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Position at bottom right with padding
        x = width - text_width - 10
        y = height - text_height - 10
        
        # Draw shadow
        draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0))
        # Draw text
        draw.text((x, y), text, font=font, fill=(255, 255, 255))

    def add_metadata(self, author: str, copyright: str, noai: str = "True"):
        """
        Add simple EXIF metadata including NoAI tags.
        """
        try:
            exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            # Copyright (Tag 0x8298)
            exif_dict["0th"][piexif.ImageIFD.Copyright] = copyright.encode('utf-8')
            
            # Artist (Tag 0x013b)
            exif_dict["0th"][piexif.ImageIFD.Artist] = author.encode('utf-8')
            
            # Software (Tag 0x0131)
            exif_dict["0th"][piexif.ImageIFD.Software] = b"ArtShield Agent 2"
            
            # UserComment (Tag 0x9286) - Often used for extra metadata
            # We will inject "NoAI" here as a persistent signal
            if noai.lower() == "true":
                # ASCII prefix for UserComment
                user_comment = b"ASCII\0\0\0NoAI: True"
                exif_dict["Exif"][piexif.ExifIFD.UserComment] = user_comment

            exif_bytes = piexif.dump(exif_dict)
            self.exif_bytes = exif_bytes
        except Exception as e:
            print(f"Failed to create metadata: {e}")
            self.exif_bytes = None

    def save(self, output_path: str):
        """
        Save the processed image to output_path.
        """
        if hasattr(self, 'exif_bytes') and self.exif_bytes:
            self.image.save(output_path, "JPEG", exif=self.exif_bytes)
        else:
            self.image.save(output_path, "JPEG")
