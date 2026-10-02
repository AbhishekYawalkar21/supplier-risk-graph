import pytest

from src.graph.queries import (
    get_company_count,
    get_supplier_company_relationships,
    get_supplier_count,
)


@pytest.mark.integration
def test_company_count():
    assert get_company_count() == 10


@pytest.mark.integration
def test_supplier_count():
    # 40 total suppliers exist in the dataset
    assert get_supplier_count() == 40


@pytest.mark.integration
def test_supplier_company_relationships():
    relationships = get_supplier_company_relationships()

    # Only 37 suppliers successfully matched to a canonical company
    assert len(relationships) == 37

    assert any(
        row["company"] == "Siemens"
        for row in relationships
    )