from fastapi import FastAPI, HTTPException
from src.rag_project.data_retrieval.chain import llm_chain
from pydantic import BaseModel
from mangum import Mangum

app = FastAPI()

class Question(BaseModel):
    question:str

@app.post("/ask")
async def get_response(query:Question):
    if not query.question:
        raise HTTPException(status_code=400, detail=f"Question is required.")
    return llm_chain(query.question)

handler = Mangum(app)
