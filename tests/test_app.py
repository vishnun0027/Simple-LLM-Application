import pytest
from fastapi.testclient import TestClient
from src.app import app  # Assuming your FastAPI app is in 'app.py'
import os

# Create a TestClient instance
client = TestClient(app)

# Test environment variables
def test_api_key_availability():
    assert os.getenv("GROQ_API_KEY"), "GROQ_API_KEY is not set!"
    assert os.getenv("LANGCHAIN_API_KEY"), "LANGCHAIN_API_KEY is not set!"

# Parameterized test for /translate/ endpoint
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"language": "Spanish", "text": "Hello, how are you?"}, 200),
        ({"language": "French", "text": "Good morning!"}, 200),
        ({"language": "", "text": "Empty language"}, 422),  # Invalid request
        ({"text": "Missing language"}, 422),  # Missing field
    ],
)
def test_translate(payload, expected_status):
    response = client.post("/translate/", json=payload)
    assert response.status_code == expected_status
    if response.status_code == 200:
        data = response.json()
        assert "translated_text" in data
        assert data["translated_text"]  # Translation should not be empty

# Parameterized test for /similar-words/ endpoint
@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"word": "happy"}, 200),
        ({"word": "joyful"}, 200),
        ({"word": ""}, 422),  # Invalid request (empty word)
        ({}, 422),  # Missing field
    ],
)
def test_similar_words(payload, expected_status):
    response = client.post("/similar-words/", json=payload)
    assert response.status_code == expected_status
    if response.status_code == 200:
        data = response.json()
        assert "similar_words" in data
        assert data["similar_words"]  # List of similar words should not be empty

