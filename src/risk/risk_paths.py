from __future__ import annotations

from src.graph.queries import find_risk_paths


def get_supplier_risk_summary(
    supplier_id: str,
) -> dict:

    paths = find_risk_paths(
        supplier_id,
        max_hops=4,
    )

    if not paths:
        return {
            "supplier_id": supplier_id,
            "has_risk": False,
            "risk_paths": [],
        }

    return {
        "supplier_id": supplier_id,
        "has_risk": True,
        "risk_paths": paths,
    }