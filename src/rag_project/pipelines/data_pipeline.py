from data_collection.raw_docs import load_all_pages
from data_collection.create_chunks import get_all_chunks
from data_collection.add_chroma import add_chroma
from src.logger import logging
from src.exception import CustomException
import sys

def data_pipeline(url_lst):
    try:
        logging.info("=" * 40)
        logging.info("STARTING DATA PIPELINE")
        logging.info("=" * 40)
        
        raw_docs = load_all_pages(url_lst)
        logging.info("RAW DOCUMENTS RETRIEVED")
        logging.info(f"Fetched {len(raw_docs)} documents")
        logging.info("-" * 40)

        all_chunks = get_all_chunks(raw_docs)
        logging.info("CHUNKS CREATED")
        logging.info(f"Created {len(all_chunks)} chunks")
        logging.info("-" * 40)

        add_chroma(all_chunks)
        logging.info("-" * 40)
        logging.info("DATA INGESTED INTO CHROMA")
        logging.info("-" * 40)

        # Pipeline end header
        logging.info("=" * 40)
        logging.info("DATA PIPELINE COMPLETE")
        logging.info("=" * 40)

    except Exception as e:
        raise CustomException(e,sys)