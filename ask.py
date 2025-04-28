from fastapi import APIRouter
from pydantic import BaseModel
from services import embedding, qdrant_search, redis_cache, llm

router = APIRouter()

class AskRequest(BaseModel):
    query: str

@router.post("/ask")
async def ask_question(request: AskRequest):
    query = request.query

    # Step 1: Embed the query
    query_embedding = embedding.embed(query)

    # Step 2: Get the latest uploaded doc_id from Redis
    doc_id = redis_cache.get_latest_doc_id()
    if not doc_id:
        return {"error": "No document found. Please upload a PDF first."}

    # Step 3: Qdrant semantic search for relevant chunks
    results = qdrant_search.semantic_search(query_embedding, doc_id=doc_id)

    # Step 4: Build context from chunks if available
    if results:
        context = "\n".join([r["text"] for r in results])
        source = "contextual"
    else:
        context = ""
        source = "llm_fallback"

    # Step 5: Call Ollama (Gemma) LLM to generate an answer
    answer = llm.generate_answer(query=query, full_context=context)

    return {
        "query": query,
        "answer": answer,
        "source": source
    }
@router.post("/search")
async def search_all_documents(request: AskRequest):
    query = request.query

    # Step 1: Embed the query
    query_embedding = embedding.embed(query)

    # Step 2: Qdrant search across all documents
    results = qdrant_search.semantic_search(query_embedding)

    # Step 3: Build context from retrieved chunks
    if results:
        context = "\n".join([r["text"] for r in results])
    else:
        context = ""

    # Step 4: Use LLM to answer based on global context
    answer = llm.generate_answer(query, full_context=context)

    return {
        "query": query,
        "answer": answer,
        "source": "global_context" if results else "llm_fallback"
    }
