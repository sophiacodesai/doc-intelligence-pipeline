import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_extract_invoice():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        with open("tests/sample_invoice.pdf", "rb") as f:
            response = await ac.post("/extract/invoice", files={"file": ("invoice.pdf", f, "application/pdf")})
        assert response.status_code == 200
