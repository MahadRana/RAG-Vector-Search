import tiktoken
from typing import List

def chunk_text(text:str, max_tokens:int=500, overlap:int=100) -> List[str]:
    if overlap > max_tokens: 
        return []
    enc = tiktoken.encoding_for_model("gpt-4o")
    all_tokens = enc.encode(text)
    chunks = []
    start = 0

    while start < len(all_tokens):
        end = start + max_tokens
        enc_chunk = all_tokens[start:end]
        chunk = enc.decode(enc_chunk)
        chunks.append(chunk)
        start = end-overlap

    
    return chunks

def make_chunk_records(chunks: List[str], doc:dict) -> List[dict]:
    records = []
    for i, chunk in enumerate(chunks):
        records.append({
            "id": f"{doc['id']}_chunk{i}",
            "text": chunk,
            "metadata": {
                **doc["metadata"],
                "chunk_index": i,        
                "source_id": doc["id"]
            }
        })
    return records

def get_all_chunks(raw_docs:List[dict]) -> List[dict]:
    all_chunks = []
    for doc in raw_docs:
        chunks = chunk_text(doc["text"])
        chunk_records = make_chunk_records(doc, chunks)
        all_chunks.extend(chunk_records)
    return all_chunks



