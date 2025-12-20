import pytest
from PIL import Image
import piexif
import os
from backend.processor import ImageProcessor, ProtectionParams, ProtectionType
import tempfile

@pytest.fixture
def sample_image():
    """Create a temporary sample image for testing."""
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        img = Image.new('RGB', (100, 100), color = 'red')
        img.save(tmp.name)
        return tmp.name

def test_metadata_injection_jpg(sample_image):
    """Test metadata injection into JPEG."""
    processor = ImageProcessor(sample_image)
    params = ProtectionParams(
        image_path=sample_image,
        protection_type=ProtectionType.TAG,
        metadata={
            "author": "Test Artist",
            "copyright": "Copyright 2025 Test",
            "noai": "True"
        }
    )
    
    # This method doesn't exist yet with this signature or functionality
    processor.process(params)
    
    # Verify metadata
    img = Image.open(processor.output_path)
    exif_dict = piexif.load(img.info['exif'])
    
    # Check Copyright (0x8298)
    assert exif_dict['0th'][piexif.ImageIFD.Copyright] == b"Copyright 2025 Test"
    
    # Check Artist (0x013b)
    assert exif_dict['0th'][piexif.ImageIFD.Artist] == b"Test Artist"
    
    # Cleanup
    os.remove(sample_image)
    if processor.output_path and os.path.exists(processor.output_path):
        os.remove(processor.output_path)

def test_metadata_noai_tag(sample_image):
    """Test specific NoAI tag injection."""
    processor = ImageProcessor(sample_image)
    params = ProtectionParams(
        image_path=sample_image,
        protection_type=ProtectionType.TAG,
        metadata={"noai": "True"}
    )
    processor.process(params)
    
    img = Image.open(processor.output_path)
    # This is a placeholder for where we expect the NoAI tag to be (e.g., UserComment or XMP)
    # For now, we will use UserComment (0x9286) as a proxy for the test until we implement XMP
    exif_dict = piexif.load(img.info['exif'])
    user_comment = exif_dict['Exif'].get(piexif.ExifIFD.UserComment, b'')
    assert b"NoAI" in user_comment

    # Cleanup
    os.remove(sample_image)
    if processor.output_path and os.path.exists(processor.output_path):
        os.remove(processor.output_path)
