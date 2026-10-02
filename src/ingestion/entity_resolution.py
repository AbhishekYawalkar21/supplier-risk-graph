from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from rapidfuzz import fuzz, process

from src.ingestion.clean import normalize_company_name


@dataclass
class MatchResult:
    company_id: str
    canonical_name: str
    score: float
    method: str


def load_companies(path: str) -> pd.DataFrame:
    companies = pd.read_csv(path)

    required_columns = {
        "company_id",
        "canonical_name",
        "legal_name",
        "country",
        "city",
        "website",
        "industry",
    }

    missing = required_columns - set(companies.columns)

    if missing:
        raise ValueError(
            f"Missing required company columns: {sorted(missing)}"
        )

    companies["canonical_match_key"] = companies["legal_name"].apply(
        normalize_company_name
    )

    companies["canonical_name_match_key"] = companies[
        "canonical_name"
    ].apply(normalize_company_name)

    return companies


def exact_match(
    supplier_name: str,
    companies: pd.DataFrame,
) -> MatchResult | None:
    key = normalize_company_name(supplier_name)

    matches = companies[
        (companies["canonical_match_key"] == key)
        | (companies["canonical_name_match_key"] == key)
    ]

    if matches.empty:
        return None

    company = matches.iloc[0]

    return MatchResult(
        company_id=company["company_id"],
        canonical_name=company["canonical_name"],
        score=1.0,
        method="exact",
    )


def fuzzy_match(
    supplier_name: str,
    companies: pd.DataFrame,
    score_cutoff: float = 70.0,
) -> MatchResult | None:
    supplier_key = normalize_company_name(supplier_name)

    # Search against the canonical name key
    choices = {
        index: value
        for index, value in companies["canonical_name_match_key"].items()
    }

    # Use partial_ratio to handle trailing truncations and abbreviations
    result = process.extractOne(
        supplier_key,
        choices,
        scorer=fuzz.partial_ratio, 
        score_cutoff=score_cutoff,
    )

    if result is None:
        return None

    _, score, index = result

    company = companies.loc[index]

    return MatchResult(
        company_id=company["company_id"],
        canonical_name=company["canonical_name"],
        score=score / 100.0,
        method="fuzzy",
    )


def resolve_supplier(
    supplier_name: str,
    companies: pd.DataFrame,
) -> MatchResult | None:
    exact = exact_match(supplier_name, companies)

    if exact:
        return exact

    return fuzzy_match(supplier_name, companies)


def resolve_all_suppliers(
    suppliers_path: str,
    companies_path: str,
    output_path: str,
) -> pd.DataFrame:
    suppliers = pd.read_csv(suppliers_path)
    companies = load_companies(companies_path)

    results = []

    for _, supplier in suppliers.iterrows():
        match = resolve_supplier(
            supplier["supplier_name"],
            companies,
        )

        if match is None:
            results.append(
                {
                    "supplier_id": supplier["supplier_id"],
                    "supplier_name": supplier["supplier_name"],
                    "matched_company_id": None,
                    "matched_company_name": None,
                    "match_score": 0.0,
                    "match_method": "unmatched",
                }
            )
        else:
            results.append(
                {
                    "supplier_id": supplier["supplier_id"],
                    "supplier_name": supplier["supplier_name"],
                    "matched_company_id": match.company_id,
                    "matched_company_name": match.canonical_name,
                    "match_score": round(match.score, 4),
                    "match_method": match.method,
                }
            )

    result_df = pd.DataFrame(results)

    result_df.to_csv(output_path, index=False)

    return result_df


if __name__ == "__main__":
    resolve_all_suppliers(
        "data/processed/suppliers_clean.csv",
        "data/raw/companies.csv",
        "data/processed/supplier_company_matches.csv",
    )