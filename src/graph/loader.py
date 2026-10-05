from __future__ import annotations
import os

from dotenv import load_dotenv
import pandas as pd
from neo4j import GraphDatabase
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


def load_companies(session, companies: pd.DataFrame) -> None:
    query = """
    UNWIND $companies AS company

    MERGE (c:Company {
        company_id: company.company_id
    })

    SET
        c.canonical_name = company.canonical_name,
        c.legal_name = company.legal_name,
        c.country = company.country,
        c.city = company.city,
        c.website = company.website,
        c.industry = company.industry,
        c.description = company.description
    """

    session.run(
        query,
        companies=companies.to_dict("records"),
    )


def load_suppliers(
    session,
    suppliers: pd.DataFrame,
    matches: pd.DataFrame,
) -> None:

    merged = suppliers.merge(
        matches[
            [
                "supplier_id",
                "matched_company_id",
                "matched_company_name",
                "match_score",
                "match_method",
            ]
        ],
        on="supplier_id",
        how="left",
    )

    query = """
    UNWIND $suppliers AS supplier

    MERGE (s:Supplier {
        supplier_id: supplier.supplier_id
    })

    SET
        s.original_name = supplier.supplier_name,
        s.normalized_name = supplier.supplier_name_normalized,
        s.country = supplier.country,
        s.city = supplier.city,
        s.category = supplier.category,
        s.match_score = supplier.match_score,
        s.match_method = supplier.match_method

    WITH s, supplier

    OPTIONAL MATCH (c:Company {
        company_id: supplier.matched_company_id
    })

    FOREACH (_ IN CASE
        WHEN c IS NOT NULL THEN [1]
        ELSE []
    END |
        MERGE (s)-[:SUPPLIES]->(c)
    )
    """

    session.run(
        query,
        suppliers=merged.to_dict("records"),
    )


def load_corporate_relationships(
    session,
    relationships: pd.DataFrame,
) -> None:

    query = """
    UNWIND $relationships AS relationship

    MATCH (parent:Company {
        company_id: relationship.parent_company_id
    })

    MATCH (child:Company {
        company_id: relationship.subsidiary_company_id
    })

    MERGE (child)-[r:SUBSIDIARY_OF]->(parent)

    SET
        r.ownership_percent =
            toFloat(relationship.ownership_percent),
        r.source = relationship.source,
        r.confidence =
            toFloat(relationship.confidence)
    """

    session.run(
        query,
        relationships=relationships.to_dict("records"),
    )


def load_risks(
    session,
    risks: pd.DataFrame,
) -> None:

    query = """
    UNWIND $risks AS risk

    MATCH (company:Company {
        company_id: risk.company_id
    })

    MERGE (r:Risk {
        risk_id: risk.risk_id
    })

    SET
        r.risk_type = risk.risk_type,
        r.risk_description = risk.risk_description,
        r.source = risk.source,
        r.effective_date = risk.effective_date,
        r.last_updated = risk.last_updated,
        r.confidence = toFloat(risk.confidence)

    MERGE (company)-[:HAS_RISK]->(r)
    """

    session.run(
        query,
        risks=risks.to_dict("records"),
    )


def load_graph() -> None:

    companies = pd.read_csv(
        "data/raw/companies.csv"
    )

    suppliers = pd.read_csv(
        "data/processed/suppliers_clean.csv"
    )

    matches = pd.read_csv(
        "data/processed/supplier_company_matches.csv"
    )

    relationships = pd.read_csv(
        "data/raw/corporate_relationships.csv"
    )

    risks = pd.read_csv(
        "data/raw/risk_entities.csv"
    )

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:
        with driver.session() as session:
            load_companies(
                session,
                companies,
            )

            load_suppliers(
                session,
                suppliers,
                matches,
            )

            load_corporate_relationships(
                session,
                relationships,
            )

            load_risks(
                session,
                risks,
            )

    finally:
        driver.close()


if __name__ == "__main__":
    load_graph()

    print(
        "Supplier Risk Graph loaded into Neo4j."
    )