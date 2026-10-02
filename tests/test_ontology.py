from pathlib import Path

import yaml


def test_ontology_exists():
    path = Path("ontology/schema.yaml")

    assert path.exists()


def test_ontology_contains_core_entities():
    path = Path("ontology/schema.yaml")

    with path.open("r", encoding="utf-8") as file:
        schema = yaml.safe_load(file)

    entities = schema["entities"]

    assert "Supplier" in entities
    assert "Company" in entities
    assert "Risk" in entities


def test_ontology_contains_core_relationships():
    path = Path("ontology/schema.yaml")

    with path.open("r", encoding="utf-8") as file:
        schema = yaml.safe_load(file)

    relationships = schema["relationships"]

    assert "SUPPLIES" in relationships
    assert "OWNS" in relationships
    assert "SUBSIDIARY_OF" in relationships
    assert "HAS_RISK" in relationships