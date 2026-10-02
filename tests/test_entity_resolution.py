
from src.ingestion.entity_resolution import (
    exact_match,
    fuzzy_match,
    load_companies,
    resolve_supplier,
)


def companies():
    return load_companies("data/raw/companies.csv")


def test_exact_match():
    result = exact_match(
        "Siemens AG",
        companies(),
    )

    assert result is not None
    assert result.company_id == "COMP-0001"
    assert result.score == 1.0


def test_fuzzy_match_typo():
    result = fuzzy_match(
        "Siemns AG",
        companies(),
    )

    assert result is not None
    assert result.company_id == "COMP-0001"
    assert result.score > 0.70


def test_resolve_supplier():
    result = resolve_supplier(
        "ABC Elec.",
        companies(),
    )

    assert result is not None
    assert result.company_id == "COMP-0002"