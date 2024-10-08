from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from the .env file
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

app = FastAPI()

# Initialize the ChatGroq model with a specific model
model = ChatGroq(model="llama3-8b-8192")

# Create a prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

# Output parser
parser = StrOutputParser()

# Create a chain
chain = prompt_template | model | parser

# Pydantic model for request body
class TranslationRequest(BaseModel):
    text: str
    language: str

# FastAPI route to handle translation requests
@app.post("/translate/")
def translate(request: TranslationRequest):
    response = chain.invoke({"language": request.language, "text": request.text})
    return {"translated_text": response}
