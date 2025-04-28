# app/services/graph.py
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "strongpass123"))

def save_entities(doc_id, text):
    with driver.session() as session:
        session.run("""
            MERGE (d:Document {id: $doc_id})
            MERGE (e:Entity {name: 'Sample'})
            MERGE (d)-[:MENTIONS]->(e)
        """, doc_id=doc_id)
        
def get_related_entities(doc_id):
    with driver.session() as session:
        result = session.run("""
            MATCH (d:Document {doc_id: $doc_id})-[:MENTIONS]->(e:Entity)
            RETURN e.name AS name
        """, doc_id=doc_id)
        return [record["name"] for record in result]
