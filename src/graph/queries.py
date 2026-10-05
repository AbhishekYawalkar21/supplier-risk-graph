from __future__ import annotations
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


def get_supplier_count() -> int:
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (s:Supplier) RETURN count(s) AS count"
            )

            record = result.single()

            return record["count"]
    finally:
        driver.close()


def get_company_count() -> int:
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        with driver.session() as session:
            result = session.run(
                "MATCH (c:Company) RETURN count(c) AS count"
            )

            record = result.single()

            return record["count"]
    finally:
        driver.close()


def get_supplier_company_relationships() -> list[dict]:
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = """
    MATCH (s:Supplier)-[:SUPPLIES]->(c:Company)
    RETURN
        s.supplier_id AS supplier_id,
        s.original_name AS supplier_name,
        c.company_id AS company_id,
        c.canonical_name AS company,
        s.match_score AS confidence,
        s.match_method AS method
    ORDER BY company
    """

    try:
        with driver.session() as session:
            result = session.run(query)

            return [record.data() for record in result]
    finally:
        driver.close()

def find_risk_paths(
    supplier_id: str,
    max_hops: int = 4,
    ) -> list[dict]:

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = """
    MATCH p = 
        (s:Supplier {
            supplier_id: $supplier_id
        })
        -[:SUPPLIES]->
        (company:Company)
        -[:SUBSIDIARY_OF*0..4]-
        (risk_company:Company)
        -[:HAS_RISK]->
        (risk:Risk)

    RETURN
        s.original_name AS supplier,
        [node IN nodes(p) |
            CASE
                WHEN node:Supplier
                    THEN node.original_name
                WHEN node:Company
                    THEN node.canonical_name
                WHEN node:Risk
                    THEN node.risk_type
            END
        ] AS path,
        risk.risk_type AS risk_type,
        risk.confidence AS risk_confidence

    ORDER BY length(p)
    """

    try:
        with driver.session() as session:
            result = session.run(
                query,
                supplier_id=supplier_id,
            )

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()

if __name__ == "__main__":
    print(
        f"Suppliers: {get_supplier_count()}"
    )

    print(
        f"Companies: {get_company_count()}"
    )

    print("\nRelationships:")

    for row in get_supplier_company_relationships():
        print(row)

    results = find_risk_paths("SUP-0001")

    for result in results:
        print(result)