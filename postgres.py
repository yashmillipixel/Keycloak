import psycopg2

conn = psycopg2.connect(dbname="pg-knowledgebase", user="postgres", password="postgres", host="localhost")

def save_metadata(metadata):
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            doc_id TEXT PRIMARY KEY,
            filename TEXT,
            pages INT
        )
    """)
    cur.execute("INSERT INTO documents (doc_id, filename, pages) VALUES (%s, %s, %s)",
                (metadata["doc_id"], metadata["filename"], metadata["pages"]))
    conn.commit()
    cur.close()
    conn.close()
    
def get_doc_metadata(doc_id):
    with conn.cursor() as cur:
        cur.execute("SELECT filename, pages FROM documents WHERE doc_id = %s", (doc_id,))
        row = cur.fetchone()
        return {"filename": row[0], "pages": row[1]} if row else {}