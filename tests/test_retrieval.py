from src.retrieval.hybrid import hybrid_search


def test_hybrid_search_returns_results():

    results = hybrid_search(
        "electronics company",
        k=5,
    )

    assert len(results) > 0

    assert "company_id" in results[0]

    assert "company" in results[0]