from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Initialize FastAPI app
app = FastAPI(title="Translation API")

# Load environment variables from the .env file
load_dotenv()

# Retrieve and set the Groq API key
groq_api_key = os.getenv("GROQ_API_KEY")
if groq_api_key is None:
    raise ValueError("GROQ_API_KEY not found in the environment variables.")
os.environ["GROQ_API_KEY"] = groq_api_key

# Initialize the model
model = ChatGroq(model="llama3-8b-8192")

# Define the Translation prompt template
Translation_system_template = "Translate the following text from English to {language}. Provide only the translation, no extra commentary or explanations."
Translation_prompt_template = ChatPromptTemplate.from_messages(
    [("system", Translation_system_template), ("user", "{text}")]
)

# Define the similar words prompt template
similarity_system_template = "Find similar words to '{word}'"
similarity_prompt_template = ChatPromptTemplate.from_messages(
    [("system", similarity_system_template), ("user", "{word}")]
)

# Chain to execute
Translation_chain = Translation_prompt_template | model | StrOutputParser()
similarity_chain = similarity_prompt_template | model | StrOutputParser()

# Define request model with stricter validation
class TranslationRequest(BaseModel):
    language: str = Field(..., min_length=1, description="Target language for translation")
    text: str = Field(..., min_length=1, description="Text to be translated")

class SimilarityRequest(BaseModel):
    word: str = Field(..., min_length=1, description="Word to find similar words for")

# Define the REST API endpoint
@app.post("/translate/")
def translate(request: TranslationRequest):
    """
    Translate the given text into the specified language.
    """
    try:
        response = Translation_chain.invoke({"language": request.language, "text": request.text})
        return {"translated_text": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/similar-words/")
def get_similar_words(request: SimilarityRequest):
    """
    Get similar words to the given word.
    """
    try:
        response = similarity_chain.invoke({"word": request.word})
        return {"similar_words": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
