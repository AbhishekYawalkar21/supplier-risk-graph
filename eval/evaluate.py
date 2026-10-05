import json

from src.retrieval.pipeline import retrieve_context as retrieve


def load_questions():
    with open(
        "eval/questions.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)


def evaluate():

    questions = load_questions()

    total = len(questions)
    correct = 0

    for item in questions:

        question = item["question"]
        expected = item["expected_risk_type"]

        result = retrieve(question)

        graph_context = result.get(
            "graph_context",
            []
        )

        found_types = []

        for record in graph_context:

            risk_type = record.get(
                "risk_type"
            )

            if risk_type:
                found_types.append(
                    risk_type
                )

        if expected in found_types:
            correct += 1

        print("\nQuestion:")
        print(question)

        print("Expected:")
        print(expected)

        print("Retrieved:")
        print(found_types)

    accuracy = (
        correct / total
        if total
        else 0
    )

    print("\nEvaluation")
    print("----------")
    print(f"Questions: {total}")
    print(f"Correct: {correct}")
    print(f"Accuracy: {accuracy:.2%}")


if __name__ == "__main__":
    evaluate()