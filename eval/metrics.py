def recall_at_k(
    retrieved,
    expected,
    k=5
):
    retrieved = retrieved[:k]

    if expected in retrieved:
        return 1.0

    return 0.0


def mean(values):

    if not values:
        return 0.0

    return sum(values) / len(values)