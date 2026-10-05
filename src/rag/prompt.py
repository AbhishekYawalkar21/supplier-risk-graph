from __future__ import annotations

from src.rag.context import format_context


def build_prompt(
    question: str,
    context: dict,
) -> str:

    evidence = format_context(
        context
    )

    return f"""
You are a procurement risk analysis assistant.

Use ONLY the supplied evidence.

Do not invent:
- Companies
- Relationships
- Risk records
- Sources
- Dates

If the evidence is insufficient, respond:

"I don't have enough evidence to determine this."

Question:
{question}

Evidence:
{evidence}

Answer requirements:

1. Give a concise answer.
2. Explain the relevant relationship path.
3. Identify whether the relationship is direct or indirect.
4. Mention the risk type if present.
5. Mention confidence when available.
6. Do not make legal determinations.
7. Do not infer facts that are not in the evidence.
"""