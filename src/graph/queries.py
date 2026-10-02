from __future__ import annotations

from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USERNAME = "neo4j"
PASSWORD = "supplier-risk-local"


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