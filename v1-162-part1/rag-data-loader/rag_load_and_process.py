import os

from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings

load_dotenv()

loader = DirectoryLoader(
    os.path.abspath("../pdf-documents"),
    glob="**/*.pdf",
    use_multithreading=True,
    show_progress=True,
    max_concurrency=50,
    loader_cls=UnstructuredPDFLoader,
)
docs = loader.load()

# Original version: this script used text-embedding-ada-002. That model still
# works, but OpenAI now presents text-embedding-3-small as its current small
# embedding model: it performs a bit better and costs less. Its vectors have
# the same length (1536). Use the same model as app/rag_chain.py.
# If you loaded the PDFs before with the old model, run this script again:
# pre_delete_collection=True replaces the old vectors with the new ones.
EMBEDDING_MODEL = "text-embedding-3-small"

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

text_splitter = SemanticChunker(
    embeddings=embeddings
)

flattened_docs = [doc[0] for doc in docs if doc]
chunks = text_splitter.split_documents(flattened_docs)

PGVector.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="collection164",
    connection_string="postgresql+psycopg://postgres@localhost:5432/database164",
    pre_delete_collection=True,
)