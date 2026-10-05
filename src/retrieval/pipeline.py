from __future__ import annotations

from src.retrieval.graph_expand import expand_company
from src.retrieval.hybrid import hybrid_search


def retrieve_context(
    query: str,
    top_k: int = 5,
) -> dict:

    search_results = hybrid_search(
        query,
        k=top_k,
    )

    graph_context = []

    for result in search_results:

        company_id = result["company_id"]

        expanded = expand_company(
            company_id
        )

        graph_context.extend(expanded)

    return {
        "query": query,
        "search_results": search_results,
        "graph_context": graph_context,
    }


if __name__ == "__main__":

    context = retrieve_context(
        "electronics company with risk"
    )

    print(context)