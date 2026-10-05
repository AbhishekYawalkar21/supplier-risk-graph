from src.rag.llm import generate_answer

if __name__ == "__main__":

    answer = generate_answer(
        """
        Explain knowledge graphs in two sentences.
        """
    )

    print(answer)