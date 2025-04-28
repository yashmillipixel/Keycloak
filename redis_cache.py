import redis
import hashlib

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def _key(text):
    return "q:" + hashlib.sha256(text.encode()).hexdigest()

def get_cached_answer(question):
    return r.get(_key(question))

def cache_answer(question, answer, expiry=3600):
    r.setex(_key(question), expiry, answer)

def store_doc_id(doc_id: str):
    r.set('latest_doc_id', doc_id)

def set_latest_doc_id(doc_id:str):
    r.set('latest_doc_id',doc_id)
    
def get_latest_doc_id():
    return r.get("latest_doc_id")