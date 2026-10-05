import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


CONSTRAINTS = [
    """
    CREATE CONSTRAINT supplier_id_unique IF NOT EXISTS
    FOR (s:Supplier)
    REQUIRE s.supplier_id IS UNIQUE
    """,
    """
    CREATE CONSTRAINT company_id_unique IF NOT EXISTS
    FOR (c:Company)
    REQUIRE c.company_id IS UNIQUE
    """,
]


def create_constraints() -> None:
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        with driver.session() as session:
            for query in CONSTRAINTS:
                session.run(query)
    finally:
        driver.close()


if __name__ == "__main__":
    create_constraints()
    print("Neo4j constraints created.")