from __future__ import annotations
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


def expand_company(
    company_id: str,
    max_hops: int = 2,
) -> list[dict]:

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = f"""
    MATCH path =
        (c:Company {{
            company_id: $company_id
        }})
        -[:SUBSIDIARY_OF*0..{max_hops}]-
        (related:Company)

    OPTIONAL MATCH
        (related)-[:HAS_RISK]->(risk:Risk)

    RETURN
        related.company_id AS company_id,
        related.canonical_name AS company,
        related.industry AS industry,
        [node IN nodes(path) |
            CASE
                WHEN node:Company
                THEN node.canonical_name
                ELSE node.company_id
            END
        ] AS path,
        collect(
            CASE
                WHEN risk IS NOT NULL
                THEN {{
                    risk_type: risk.risk_type,
                    description: risk.risk_description,
                    confidence: risk.confidence
                }}
            END
        ) AS risks
    """

    try:

        with driver.session() as session:

            result = session.run(
                query,
                company_id=company_id,
            )

            return [
                record.data()
                for record in result
            ]

    finally:
        driver.close()