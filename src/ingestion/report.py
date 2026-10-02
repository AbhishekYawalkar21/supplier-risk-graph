from __future__ import annotations

import pandas as pd


def generate_resolution_report(path: str) -> None:
    df = pd.read_csv(path)

    total = len(df)

    exact = (df["match_method"] == "exact").sum()
    fuzzy = (df["match_method"] == "fuzzy").sum()
    unmatched = (df["match_method"] == "unmatched").sum()

    print("\n=== Entity Resolution Report ===")
    print(f"Total suppliers : {total}")
    print(f"Exact matches   : {exact}")
    print(f"Fuzzy matches   : {fuzzy}")
    print(f"Unmatched       : {unmatched}")

    if total:
        print(f"Match rate      : {(total - unmatched) / total:.2%}")

    print("\nLow-confidence matches:")

    low_confidence = df[
        (df["match_score"] > 0)
        & (df["match_score"] < 0.85)
    ]

    if low_confidence.empty:
        print("None")
    else:
        print(
            low_confidence[
                [
                    "supplier_id",
                    "supplier_name",
                    "matched_company_name",
                    "match_score",
                ]
            ].to_string(index=False)
        )


if __name__ == "__main__":
    generate_resolution_report(
        "data/processed/supplier_company_matches.csv"
    )