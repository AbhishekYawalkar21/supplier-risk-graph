from __future__ import annotations

from src.rag.llm import generate_answer
from src.rag.prompt import build_prompt
from src.retrieval.pipeline import retrieve_context


def answer_question(
    question: str,
) -> dict:

    context = retrieve_context(
        question
    )

    prompt = build_prompt(
        question,
        context,
    )

    answer = generate_answer(
        prompt
    )

    return {
        "question": question,
        "answer": answer,
        "sources": context["search_results"],
        "graph_evidence": context["graph_context"],
    }


if __name__ == "__main__":

    result = answer_question(
        "Why is Siemens potentially risky?"
    )

    print("\nQUESTION:")
    print(result["question"])

    print("\nANSWER:")
    print(result["answer"])

    print("\nGRAPH EVIDENCE:")

    for evidence in result["graph_evidence"]:
        print(evidence)