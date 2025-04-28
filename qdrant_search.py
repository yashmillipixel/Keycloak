from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, Filter, PointStruct

client = QdrantClient(host="localhost", port=6333)

def semantic_search(query_embedding, doc_id=None, top_k=10):
    filter_ = None
    if doc_id:
        filter_ = Filter(must=[{"key": "doc_id", "match": {"value": doc_id}}])

    hits = client.search(
        collection_name="pdf_documents",
        query_vector=query_embedding,
        limit=top_k,
        query_filter=filter_
    )
    return [{"text": hit.payload["text"], "score": hit.score} for hit in hits]