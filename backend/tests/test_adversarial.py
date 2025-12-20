import pytest
from PIL import Image
import numpy as np
import os
from backend.processor import ImageProcessor, ProtectionParams, ProtectionType, Intensity

@pytest.fixture
def sample_image_path():
    """Create a temporary sample image."""
    path = "test_adversarial_input.jpg"
    img = Image.new('RGB', (256, 256), color='green')
    img.save(path)
    yield path
    if os.path.exists(path):
        os.remove(path)

def test_adversarial_cloak_applied(sample_image_path):
    """Test that CLOAK applies some change to pixels."""
    processor = ImageProcessor(sample_image_path)
    
    # Get original pixels
    original_pixels = np.array(processor.image)
    
    params = ProtectionParams(
        image_path=sample_image_path,
        protection_type=ProtectionType.CLOAK,
        intensity=Intensity.HIGH
    )
    result = processor.process(params)
    
    assert result.success is True
    
    # Load protected image and check pixels
    protected_img = Image.open(result.protected_path)
    protected_pixels = np.array(protected_img)
    
    # Check that pixels are actually different (adversarial noise added)
    assert not np.array_equal(original_pixels, protected_pixels)
    
    if os.path.exists(result.protected_path):
        os.remove(result.protected_path)

def test_adversarial_poison_applied(sample_image_path):
    """Test that POISON applies some change to pixels."""
    processor = ImageProcessor(sample_image_path)
    original_pixels = np.array(processor.image)
    
    params = ProtectionParams(
        image_path=sample_image_path,
        protection_type=ProtectionType.POISON,
        intensity=Intensity.MEDIUM
    )
    result = processor.process(params)
    
    assert result.success is True
    protected_img = Image.open(result.protected_path)
    protected_pixels = np.array(protected_img)
    
    assert not np.array_equal(original_pixels, protected_pixels)
    
    if os.path.exists(result.protected_path):
        os.remove(result.protected_path)
