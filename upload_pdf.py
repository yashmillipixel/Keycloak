import io 
from fastapi import APIRouter, UploadFile, File
from PyPDF2 import PdfReader
from services import embedding, postgres, graph, redis_cache
from services.embedding import save_to_qdrant, create_collection_if_not_exists
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    contents = await file.read()
    pdf = PdfReader(io.BytesIO(contents))

    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""

    doc_id = str(uuid.uuid4())
    metadata = {
        "filename": file.filename,
        "pages": len(pdf.pages),
        "doc_id": doc_id
    }
    
    # Store doc ID in Redis
    redis_cache.store_doc_id(doc_id)
    redis_cache.set_latest_doc_id(doc_id)

    # Save metadata to Postgres
    postgres.save_metadata(metadata)

    # Split text into chunks
    chunks = embedding.split_text(text)

    # Generate embeddings for each chunk
    embeddings = [embedding.embed(chunk) for chunk in chunks]

    # Prepare metadata per chunk
    chunk_metadata = [{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]

    # Ensure Qdrant collection exists
    create_collection_if_not_exists()

    # Save to Qdrant
    save_to_qdrant(chunks, embeddings, chunk_metadata)

    # Save entity relationships to Neo4j
    graph.save_entities(doc_id, text)

    return {"status": "uploaded", "doc_id": doc_id}
