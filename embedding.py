from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import hashlib
import numpy as np
import uuid

# Initialize Qdrant client and SentenceTransformer model
qdrant = QdrantClient("localhost", port=6333)
model = SentenceTransformer('all-MiniLM-L6-v2')  # You can choose other models

def split_text(text:str, chunk_size=300,overlap=50):
    """
    Splits the input text into chunks of the specified size.
    """ 
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def embed(text:str)-> np.ndarray:
    """
    Converts a text chunk into a vector embedding using Sentence-Transformer.
    """
    embedding = model.encode(text)
    return embedding

COLLECTION_NAME = "pdf_documents"

def create_collection_if_not_exists():
    if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE)  # 384 if using MiniLM
        )

def save_to_qdrant(text_chunks: list, embeddings: list, metadata_list: list):
    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk, **metadata}
        )
        for chunk, embedding, metadata in zip(text_chunks, embeddings, metadata_list)
    ]
    qdrant.upsert(collection_name=COLLECTION_NAME, points=points)