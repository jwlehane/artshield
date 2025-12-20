import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os
from PIL import Image
import io

client = TestClient(app)

@pytest.fixture
def sample_image_bytes():
    """Create a sample image in memory."""
    img = Image.new('RGB', (100, 100), color='blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()

def test_health_check():
    """Verify health check endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "ArtShield Backend (Agent 2) is running"}

def test_process_image_endpoint(sample_image_bytes):
    """Test the unified process endpoint with multipart form data."""
    # We expect the API to accept protection parameters as form fields or JSON
    # For simplicity in this test, we'll send a file and some form fields
    files = {'file': ('test.jpg', sample_image_bytes, 'image/jpeg')}
    data = {
        'protection_type': 'cloak_and_tag',
        'intensity': 'high',
        'metadata': '{"author": "API Test", "noai": "True"}'
    }
    
    response = client.post("/api/process", files=files, data=data)
    
    # This might fail initially if the endpoint isn't fully updated
    assert response.status_code == 200
    json_data = response.json()
    assert json_data['status'] == 'success'
    assert 'processed_url' in json_data
    assert json_data['original_filename'] == 'test.jpg'

def test_process_invalid_file():
    """Test sending a non-image file."""
    files = {'file': ('test.txt', b'not an image', 'text/plain')}
    response = client.post("/api/process", files=files)
    assert response.status_code == 400
    assert "File must be an image" in response.json()['detail']
