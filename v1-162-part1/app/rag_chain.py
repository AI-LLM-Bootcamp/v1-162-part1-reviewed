import os
from operator import itemgetter
from typing import TypedDict

from dotenv import load_dotenv
from langchain_community.vectorstores.pgvector import PGVector
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()  # the .env file must contain the line OPENAI_API_KEY=...

# Original version: this project used gpt-4-1106-preview to answer.
# OpenAI has since retired that model. Today we use a current chat model.
MODEL = "gpt-6-luna"  # small, fast and affordable current OpenAI model

# Original version: OpenAIEmbeddings() used its default model,
# text-embedding-ada-002. That model still works, but OpenAI now presents
# text-embedding-3-small as its current small embedding model: it performs
# a bit better and costs less. Its vectors have the same length (1536).
# Use the same model as rag-data-loader/rag_load_and_process.py: the question
# and the stored chunks must be turned into vectors with the same model.
EMBEDDING_MODEL = "text-embedding-3-small"

vector_store = PGVector(
    collection_name="collection164",
    connection_string="postgresql+psycopg://postgres@localhost:5432/database164",
    embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL)
)

template = """
Answer given the following context:
{context}

Question: {question}
"""

ANSWER_PROMPT = ChatPromptTemplate.from_template(template)

# The original used temperature=0 to get more stable answers.
# Recent OpenAI models only accept the default value (1), and this version
# of langchain-openai would send 0.7 if we did not write it.
# That is why we set temperature=1 explicitly.
llm = ChatOpenAI(temperature=1, model=MODEL, streaming=True)


class RagInput(TypedDict):
    question: str


final_chain = (
    {
    "context": (itemgetter("question") | vector_store.as_retriever()),
    "question": itemgetter("question")
    }
    | ANSWER_PROMPT
    | llm
    | StrOutputParser()
).with_types(input_type=RagInput)