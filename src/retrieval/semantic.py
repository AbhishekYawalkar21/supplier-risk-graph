from __future__ import annotations
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from src.retrieval.embeddings import embed_text
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


def semantic_search(
    query_text: str,
    k: int = 5,
) -> list[dict]:

    embedding = embed_text(query_text)

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = """
    CALL db.index.vector.queryNodes(
        'company_embedding',
        $k,
        $embedding
    )
    YIELD node, score

    RETURN
        node.company_id AS company_id,
        node.canonical_name AS company,
        node.industry AS industry,
        node.description AS description,
        score

    ORDER BY score DESC
    """

    try:

        with driver.session() as session:

            result = session.run(
                query,
                k=k,
                embedding=embedding,
            )

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()


if __name__ == "__main__":

    results = semantic_search(
        "electronics manufacturing"
    )

    for result in results:
        print(result)