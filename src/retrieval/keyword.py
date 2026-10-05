from __future__ import annotations
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


def keyword_search(
    query_text: str,
    k: int = 5,
) -> list[dict]:

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = """
    CALL db.index.fulltext.queryNodes(
        'company_fulltext',
        $query
    )
    YIELD node, score

    RETURN
        node.company_id AS company_id,
        node.canonical_name AS company,
        node.industry AS industry,
        node.description AS description,
        score

    ORDER BY score DESC
    LIMIT $k
    """

    try:

        with driver.session() as session:

            result = session.run(
                query,
                parameters={
                    "query": query_text,
                    "k": k
                }
            )

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()


if __name__ == "__main__":

    results = keyword_search(
        "Siemens"
    )

    for result in results:
        print(result)