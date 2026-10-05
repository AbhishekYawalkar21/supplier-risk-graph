from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.rag.answer import answer_question
from src.risk.risk_paths import get_supplier_risk_summary
from src.graph.queries import find_risk_paths


app = FastAPI(
    title="Supplier Risk Graph API",
    description="Evidence-grounded supplier risk investigation API",
    version="1.0.0",
)


class RiskQuery(BaseModel):
    question: str


class SupplierRiskRequest(BaseModel):
    supplier_id: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "supplier-risk-graph"
    }


@app.post("/ask")
def ask_question(request: RiskQuery):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    result = answer_question(request.question)

    return result


@app.post("/supplier/risk")
def supplier_risk(request: SupplierRiskRequest):
    if not request.supplier_id.strip():
        raise HTTPException(
            status_code=400,
            detail="Supplier ID cannot be empty."
        )

    result = get_supplier_risk_summary(
        request.supplier_id
    )

    return {
        "supplier_id": request.supplier_id,
        "risk_paths": result
    }

@app.get("/supplier/{supplier_id}/investigate")
def investigate_supplier(supplier_id: str):
    risk_paths = find_risk_paths(
        supplier_id,
        max_hops=4
    )

    return {
        "supplier_id": supplier_id,
        "risk_found": len(risk_paths) > 0,
        "risk_path_count": len(risk_paths),
        "risk_paths": risk_paths,
    }