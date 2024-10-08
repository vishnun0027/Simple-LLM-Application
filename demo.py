from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from the .env file
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = groq_api_key

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

# Invoke the chain
output = chain.invoke({"language": "italian", "text": "hi"})
print(output)
