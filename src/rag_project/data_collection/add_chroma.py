from typing import List
from chromadb import PersistentClient
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE
from src.logger import logging
from src.exception import CustomException
import sys

client = PersistentClient(
    path = './chroma_db',
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

collection = client.get_or_create_collection(name='RAG_Vector')

def add_chroma(all_chunks:List[dict]):
    try:
        logging.info(f"add_chroma: Starting ingestion of {len(all_chunks)} chunks into 'RAG_Vector'")
        collection.add(
            ids = [chunk['id'] for chunk in all_chunks],
            documents = [chunk['text'] for chunk in all_chunks],
            metadatas = [chunk['metadata'] for chunk in all_chunks]
        )
        logging.info("add_chroma: Ingestion complete, all chunks added to DB successfully!")
    except Exception as e:
        logging.error("Ingestion failed", exc_info=True)
        raise CustomException(e, sys)
