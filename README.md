# Build a Simple LLM Application
A FastAPI-based application that provides translation and word similarity services using LangChain and the Groq LLM API.

## Features

- Text translation to multiple languages
- Finding similar words for a given input word
- RESTful API endpoints
- Input validation using Pydantic models
- Error handling with proper HTTP status codes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vishnun0027/Simple-LLM-Application.git
cd Simple-LLM-Application
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

1. Start the server:
```bash
uvicorn src.app:app --reload
```

2. The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Translation Endpoint

**POST** `/translate/`

Translates text from English to a specified language.

Request body:
```json
{
    "language": "Spanish",
    "text": "Hello, how are you?"
}
```

Response:
```json
{
    "translated_text": "Hola, ¿cómo estás?"
}
```

### 2. Similar Words Endpoint

**POST** `/similar-words/`

Finds similar words to the input word.

Request body:
```json
{
    "word": "happy"
}
```

Response:
```json
{
    "similar_words": "joyful, cheerful, delighted, content, pleased..."
}
```

## Error Handling

The API includes proper error handling with appropriate HTTP status codes:

- `400 Bad Request`: Invalid input data
- `500 Internal Server Error`: Server-side processing errors