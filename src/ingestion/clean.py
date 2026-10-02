from __future__ import annotations

import re
import unicodedata

import pandas as pd


COMPANY_SUFFIXES = [
    "aktiengesellschaft",
    "gesellschaft mit beschränkter haftung",
    "gmbh",
    "ag",
    "ltd",
    "limited",
    "llc",
    "inc",
    "incorporated",
    "corp",
    "corporation",
]


def normalize_text(value: object) -> str:
    """Normalize text for matching while preserving the original value elsewhere."""
    if value is None or pd.isna(value):
        return ""

    text = str(value).strip().lower()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        character
        for character in text
        if not unicodedata.combining(character)
    )

    text = text.replace("&", " and ")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def normalize_company_name(value: object) -> str:
    """Normalize a company name and remove common legal suffixes."""
    text = normalize_text(value)

    for suffix in COMPANY_SUFFIXES:
        pattern = rf"\b{re.escape(suffix)}\b"
        text = re.sub(pattern, " ", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def clean_supplier_data(input_path: str, output_path: str) -> pd.DataFrame:
    """Read, clean and enrich the supplier CSV."""
    df = pd.read_csv(input_path)

    required_columns = {
        "supplier_id",
        "supplier_name",
        "address",
        "country",
        "city",
        "postal_code",
        "website",
        "category",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    df["supplier_name_original"] = df["supplier_name"]

    df["supplier_name_normalized"] = df["supplier_name"].apply(
        normalize_text
    )

    df["supplier_name_match_key"] = df["supplier_name"].apply(
        normalize_company_name
    )

    df["country_normalized"] = df["country"].apply(normalize_text)
    df["city_normalized"] = df["city"].apply(normalize_text)

    df["website_normalized"] = (
        df["website"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    df["address_normalized"] = df["address"].apply(normalize_text)

    df.to_csv(output_path, index=False)

    return df


if __name__ == "__main__":
    clean_supplier_data(
        "data/raw/suppliers.csv",
        "data/processed/suppliers_clean.csv",
    )