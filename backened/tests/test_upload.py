import io
from fastapi.testclient import TestClient
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import app

client = TestClient(app)


def test_upload_rejects_unsupported_file_type():
    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "error"
