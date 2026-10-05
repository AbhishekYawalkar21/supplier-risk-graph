from __future__ import annotations


def format_context(context: dict) -> str:

    lines = []

    lines.append(
        f"User query: {context['query']}"
    )

    lines.append("\nRelevant companies:")

    for result in context["search_results"]:

        lines.append(
            f"""
Company: {result['company']}
Company ID: {result['company_id']}
Industry: {result['industry']}
Retrieval score: {result.get('hybrid_score', 0):.4f}
Description: {result['description']}
"""
        )

    lines.append("\nGraph evidence:")

    for item in context["graph_context"]:

        lines.append(
            f"""
Company: {item['company']}
Company ID: {item['company_id']}
Path: {' -> '.join(item['path'])}
Risks: {item['risks']}
"""
        )

    return "\n".join(lines)