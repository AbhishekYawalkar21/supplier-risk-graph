from __future__ import annotations
import os

from dotenv import load_dotenv
import pandas as pd
from neo4j import GraphDatabase

from src.retrieval.embeddings import embed_text
from src.config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD

load_dotenv()

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "supplier-risk-local")


def create_vector_index() -> None:

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = """
    CREATE VECTOR INDEX company_embedding IF NOT EXISTS
    FOR (c:Company)
    ON c.embedding
    OPTIONS {
        indexConfig: {
            `vector.dimensions`: 1024,
            `vector.similarity_function`: 'cosine'
        }
    }
    """

    try:
        with driver.session() as session:
            session.run(query)

    finally:
        driver.close()


def create_fulltext_index() -> None:

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    query = """
    CREATE FULLTEXT INDEX company_fulltext IF NOT EXISTS
    FOR (c:Company)
    ON EACH [
        c.canonical_name,
        c.legal_name,
        c.industry,
        c.description
    ]
    """

    try:
        with driver.session() as session:
            session.run(query)

    finally:
        driver.close()


def embed_companies() -> None:

    companies = pd.read_csv(
        "data/raw/companies.csv"
    )

    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD),
    )

    try:

        with driver.session() as session:

            for _, company in companies.iterrows():

                text = (
                    f"Company: {company['canonical_name']}. "
                    f"Legal name: {company['legal_name']}. "
                    f"Industry: {company['industry']}. "
                    f"Country: {company['country']}. "
                    f"Description: {company['description']}"
                )

                embedding = embed_text(text)

                session.run(
                    """
                    MATCH (c:Company {
                        company_id: $company_id
                    })

                    SET c.embedding = $embedding
                    """,
                    company_id=company["company_id"],
                    embedding=embedding,
                )

    finally:
        driver.close()


if __name__ == "__main__":

    print("Creating vector index...")
    create_vector_index()

    print("Creating full-text index...")
    create_fulltext_index()

    print("Generating company embeddings...")
    embed_companies()

    print("Semantic indexes ready.")