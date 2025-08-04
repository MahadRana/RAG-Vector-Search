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

def get_most_relevant(query, num_results=3):
    try:
        logging.info(f"get_most_relevant: Retrieve {num_results} relevant pages for query:{query}")

        documents = collection.query(
            query_texts = [query],
            n_results = num_results
        )
        logging.info("get_most_relevant: Data retrieval complete!")
        return documents
    except Exception as e:
        logging.error(f"get_most_relevant: Retrieval for relevant pages failed.", exc_info=True)
        raise CustomException(e,sys)