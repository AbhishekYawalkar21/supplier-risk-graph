from src.ingestion.clean import (
    normalize_company_name,
    normalize_text,
)


def test_normalize_text():
    assert normalize_text("  Siemens AG  ") == "siemens ag"


def test_normalize_punctuation():
    assert normalize_text("A.B.C Electronics") == "a b c electronics"


def test_remove_company_suffix():
    assert normalize_company_name("Siemens AG") == "siemens"


def test_remove_ltd_suffix():
    assert normalize_company_name("Northstar Components Ltd.") == (
        "northstar components"
    )


def test_remove_gmbh_suffix():
    assert normalize_company_name("Contoso Manufacturing GmbH") == (
        "contoso manufacturing"
    )