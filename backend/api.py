from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# Import RAG functions
from rag_pipeline import query_rag, upsert_document, PINECONE_INDEX_NAME

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class IngestRequest(BaseModel):
    document_path: str

# --- API Endpoints ---

@app.post("/ingest")
def ingest_document_api(request: IngestRequest):
    """Endpoint to ingest a new document."""
    try:
        upsert_document(request.document_path, PINECONE_INDEX_NAME)
        return {"status": "success", "message": "Document ingested successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/query")
def query_document_api(request: QueryRequest):
    """Endpoint to query the RAG system."""
    try:
        answer = query_rag(request.question, PINECONE_INDEX_NAME)
        return {"answer": answer}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)