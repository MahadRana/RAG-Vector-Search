import tiktoken
from typing import List
from src.logger import logging
from src.exception import CustomException
import sys

def chunk_text(text:str, id: str, max_tokens:int=500, overlap:int=100) -> List[str]:
    logging.info(f"chunk_text: Creating chunks for {id}")
    if overlap > max_tokens: 
        logging.debug(f"chunk_text: Overlap {overlap} greater than max number of tokens {max_tokens}")
        return []
    try:
        enc = tiktoken.encoding_for_model("gpt-4o")
        all_tokens = enc.encode(text)
    except Exception as e:
        logging.debug(f"chunk_text: Error Encoding Text {id}: {e}", exc_info=True)
        raise CustomException(e,sys)
    
    logging.info("chunk_text: Text encoded for the LLM")
    chunks = []
    start = 0
    chunk_num = 1
    while start < len(all_tokens):
        end = start + max_tokens
        end = min(end, all_tokens)
        try:
            enc_chunk = all_tokens[start:end]
            chunk = enc.decode(enc_chunk)
        except Exception as e:
            logging.debug(f"chunk_text: Error Decoding Text {id}: {e}", exc_info=True)
            raise CustomException(e,sys)
        chunks.append(chunk)
        logging.info(f"chunk_text: Chunk {chunk_num} successfully created")
        chunk_num += 1
        start = end-overlap
    logging.info("chunk_text: All chunks created!")
    return chunks

def make_chunk_records(chunks: List[str], doc:dict) -> List[dict]:
    logging.info(f"make_chunk_records: Creating records for {doc['id']}")
    records = []
    for i, chunk in enumerate(chunks):
        try:
            records.append({
                "id": f"{doc['id']}_chunk{i}",
                "text": chunk,
                "metadata": {
                    **doc["metadata"],
                    "chunk_index": i,        
                    "source_id": doc["id"]
                }
            })
        except Exception as e:
            logging.debug(f"make_chunk_records: error in creating a record for chunk {i+1}", exc_info=True)
            raise CustomException(e,sys)
    logging.info("make_chunk_records: All records successfully created!")
    return records

def get_all_chunks(raw_docs:List[dict]) -> List[dict]:
    logging.info(f"get_all_chunks: Creating Chunks for {len(raw_docs)} pages")
    all_chunks = []
    for idx, doc in enumerate(raw_docs):
        logging.info(f"get_all_chunks: loading doc {idx+1}/{len(raw_docs)}: {doc['id']}")
        chunks = chunk_text(doc["text"], doc["id"])
        chunk_records = make_chunk_records(chunks=chunks, doc=doc)
        all_chunks.extend(chunk_records)
    
    logging.info("load_all_pages: all chunks successfully created!")
    return all_chunks



