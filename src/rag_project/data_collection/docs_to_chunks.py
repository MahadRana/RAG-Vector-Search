from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from src.rag_project.data_collection.raw_docs import load_html_page
from langchain_core.documents import Document
from src.logger import logging
from src.exception import CustomException
import sys
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.environ.get("API_KEY")

EMBED_MODEL = "text-embedding-3-small"   
embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key = OPENAI_API_KEY)

vectordb = Chroma(
    collection_name="RAG_Vector_openai",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    length_function=len,  # character-based; switch to token-based if needed
)

def clean_text(t: str) -> str:
    t = " ".join(t.split())           # collapse whitespace
    return t.strip()

def chunk_text(url:str):
    logging.info(f"chunk_text: Creating chunks for {url}")
    raw_text_unclean = load_html_page(url)
    raw_text = clean_text(raw_text_unclean)
    try:
        document = Document(
            page_content=raw_text,
            metadata={"source": url}
        )
        chunks = splitter.split_documents([document])
        if not chunks:
            logging.warning(f"chunk_text: No chunks produced for {url}")
            return []
        
        logging.info(f"chunk_text: Produced {len(chunks)} chunks for {url}")
        for idx, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = f"{url}_chunk{idx}"
        return chunks
    except Exception as e:
        logging.error(f"chunk_text: Error Encoding Text {url}: {e}", exc_info=True)
        raise CustomException(e,sys)
    




