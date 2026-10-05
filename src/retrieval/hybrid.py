from __future__ import annotations

from src.retrieval.keyword import keyword_search
from src.retrieval.semantic import semantic_search


def reciprocal_rank_fusion(
    result_lists: list[list[dict]],
    k: int = 60,
) -> list[dict]:

    scores: dict[str, float] = {}
    documents: dict[str, dict] = {}

    for results in result_lists:

        for rank, result in enumerate(results, start=1):

            company_id = result["company_id"]

            scores[company_id] = (
                scores.get(company_id, 0.0)
                + 1.0 / (k + rank)
            )

            documents[company_id] = result

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    output = []

    for company_id, score in ranked:

        document = documents[company_id].copy()

        document["hybrid_score"] = score

        output.append(document)

    return output


def hybrid_search(
    query: str,
    k: int = 5,
) -> list[dict]:

    semantic_results = semantic_search(
        query,
        k=k,
    )

    keyword_results = keyword_search(
        query,
        k=k,
    )

    fused = reciprocal_rank_fusion(
        [
            semantic_results,
            keyword_results,
        ]
    )

    return fused[:k]


if __name__ == "__main__":

    results = hybrid_search(
        "Siemens"
    )

    for result in results:
        print(result)