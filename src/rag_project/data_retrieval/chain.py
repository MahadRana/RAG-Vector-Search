import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings



load_dotenv()

OPENAI_API_KEY = os.environ.get("API_KEY")
OPENAI_MODEL = os.environ.get("MODEL_NAME")

llm = ChatOpenAI(openai_api_key = OPENAI_API_KEY, model=OPENAI_MODEL)

EMBED_MODEL = "text-embedding-3-small"   
embeddings = OpenAIEmbeddings(model=EMBED_MODEL, api_key = OPENAI_API_KEY)

parser = JsonOutputParser()

vectordb = Chroma(
    collection_name="RAG_Vector_openai",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)

retriever = vectordb.as_retriever(search_kwargs={"k": 6})

template = ChatPromptTemplate([
    ("system", "You are a PC Troubleshooting Assistant. Only return valid JSON in the form: "
    "{{\"answer\": string, \"sources\": [string]}}"),
    ("human", "Use the following excerpts to answer the question. Cite sources verbatim. "
    "If the answer is not found, return {{\"answer\":\"I don\'t know\",\"sources\":[]}}. "
    "Excerpts: {retrieved_passages}. Question: {question}")
])

def format_docs(docs):
    return "\n\n".join(f"{doc.page_content}\n(source: {doc.metadata.get('source')})"
                       for doc in docs)


def llm_chain(question):
    chain = {"retrieved_passages": retriever | format_docs, "question":RunnablePassthrough()} | template | llm | parser
    return chain.invoke(question)
    
if __name__ == "__main__":
    question = "How do I fix a PC that won't turn on?"

    result = llm_chain(question)

    print("Answer:", result.get("answer"))
    print("Sources:", result.get("sources"))




