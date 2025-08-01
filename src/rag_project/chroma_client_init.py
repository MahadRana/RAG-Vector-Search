from chromadb import PersistentClient
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from src.logger import logging

client = PersistentClient(
    path = './chroma_db',
    tenant=DEFAULT_TENANT,
    database=DEFAULT_DATABASE,
)

logging.info("Client Created")

collection = client.get_or_create_collection(name='RAG_Vector')
logging.info("Vector Collection Created/Retrieved")
