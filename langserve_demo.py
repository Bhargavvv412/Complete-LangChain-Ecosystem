import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
import uvicorn

# loading dot env
load_dotenv()

# Initialize Gemini with LangChain wrapper
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
  
parser = StrOutputParser()

system_template = "Translate the following into {language}:"

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])

chain = prompt_template | llm | parser

app= FastAPI(
    title="simpleTranslator",
    version="1.0",
    description="A simple API server using Langchain's Runnable interfaces"
)

add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == "__main__":
    uvicorn.run(app,host="localhost",port=8000)