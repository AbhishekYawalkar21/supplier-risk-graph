from src.graph.queries import find_risk_paths


def test_supplier_risk_path():

    paths = find_risk_paths(
        "SUP-0001"
    )

    assert isinstance(paths, list)

    if paths:
        assert "supplier" in paths[0]
        assert "risk_type" in paths[0]