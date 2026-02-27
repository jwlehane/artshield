import pytest
from httpx import ASGITransport, AsyncClient
from backend.main import app
try:
    from backend.database import init_db
except ImportError:
    from database import init_db
import io
from PIL import Image

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

@pytest.mark.anyio
async def test_strip_metadata_endpoint():
    # Create a dummy image with some metadata
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', exif=b"some metadata")
    img_byte_arr.seek(0)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
        response = await ac.post("/api/protect/strip-metadata", files=files)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "image/jpeg"
    
    # Verify metadata is stripped
    resp_img = Image.open(io.BytesIO(response.content))
    assert resp_img.info.get('exif') is None

@pytest.mark.anyio
async def test_watermark_endpoint():
    img = Image.new('RGB', (100, 100), color = 'blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = {'file': ('test.jpg', img_byte_arr, 'image/jpeg')}
        response = await ac.post("/api/watermark", files=files)
    
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/jpeg"

@pytest.mark.anyio
async def test_process_endpoint():
    img = Image.new('RGB', (100, 100), color = 'green')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = [('files', ('test.jpg', img_byte_arr, 'image/jpeg'))]
        response = await ac.post("/api/process", files=files)
    
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["status"] == "accepted"
    return data["id"]

@pytest.mark.anyio
async def test_status_endpoint():
    # First, start a process
    img = Image.new('RGB', (100, 100), color = 'green')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        files = [('files', ('test.jpg', img_byte_arr, 'image/jpeg'))]
        response = await ac.post("/api/process", files=files)
        task_id = response.json()["id"]

        # Now check status
        status_response = await ac.get(f"/api/status/{task_id}")
        assert status_response.status_code == 200
        data = status_response.json()
        assert data["id"] == task_id
        assert "status" in data
        assert "progress" in data

