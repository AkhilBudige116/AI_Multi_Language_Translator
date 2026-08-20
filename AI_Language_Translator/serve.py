from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()


# --------BCKND SETUP--------
groq_api_key = os.getenv("GROQ_API_KEY")
model = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api_key)

# 1.Create prompt template
system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")])

parser =StrOutputParser()

# Create chain
chain = prompt_template | model | parser

# App definition
app = FastAPI(title="LangChain Serve Example",
               description="An example of using LangChain Serve with FastAPI",
                 version="0.1.0")

# Adding chain routes to the FastAPI app
add_routes(app,chain, path="/chain")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)