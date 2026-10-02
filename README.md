# Supplier Risk Graph

## Customer Problem

Procurement teams often receive supplier data from ERP systems containing
duplicate names, inconsistent legal names, spelling errors and incomplete
information.

This makes it difficult to reliably connect supplier records to canonical
companies and investigate corporate relationships.

## Project Goal

Supplier Risk Graph is an enterprise AI proof-of-concept that resolves
messy supplier records to canonical companies and represents supplier and
corporate relationships as a knowledge graph.

The later stages of the project will add risk intelligence, semantic search,
GraphRAG and explainable risk analysis.


## Architecture

Raw Supplier Data
       |
       v
Data Cleaning
       |
       v
Entity Resolution
       |
       v
Canonical Companies
       |
       v
Knowledge Graph
       |
       v
Neo4j

## Technology

- Python
- pandas
- RapidFuzz
- Neo4j Community Edition
- Docker
- Cypher
- Pytest
- Ruff

## Data

The current supplier and company data is synthetic demonstration data.

It should not be interpreted as real supplier, ownership or sanctions data.