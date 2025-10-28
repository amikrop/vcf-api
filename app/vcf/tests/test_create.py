import pytest
from django.conf import settings
from pysam import VariantFile

from vcf.tests.utils import assert_variant_not_in_file, record_to_data


def test_create_success(client_authed):
    new_variant = {
        "CHROM": "chr3",
        "POS": 40000,
        "ID": "rs987654321",
        "REF": "A",
        "ALT": "T",
    }
    response = client_authed.post("/", data=new_variant)

    with VariantFile(settings.VCF_FILE_PATH) as infile:
        for rec in infile.fetch():
            last_record = rec

    assert response.status_code == 201
    assert response.json() == new_variant
    assert record_to_data(last_record) == new_variant


def test_create_unauthorized(client):
    new_variant = {
        "CHROM": "chr1",
        "POS": 38000,
        "ID": "rs987654322",
        "REF": "G",
        "ALT": "T",
    }
    response = client.post("/", data=new_variant)

    assert response.status_code == 403
    assert_variant_not_in_file(new_variant)


def test_create_invalid_data(client_authed):
    invalid_variant = {
        "CHROM": "chrX",
        "POS": -100,
        "ID": "invalid_id",
        "REF": "B",
        "ALT": "Z",
    }
    response = client_authed.post("/", data=invalid_variant)

    assert response.status_code == 400
    assert response.json() == {
        "pos": ["Ensure this value is greater than or equal to 1."],
        "id": ["ID must be in the form 'rs<integer>'."],
        "ref": ["REF must be one of 'A', 'C', 'G', 'T', or '.'."],
        "alt": ["ALT must be one of 'A', 'C', 'G', 'T', or '.'."],
    }
    assert_variant_not_in_file(invalid_variant)


@pytest.mark.parametrize("missing_field", ["CHROM", "POS", "ID", "REF", "ALT"])
def test_create_missing_field(client_authed, missing_field):
    new_variant = {
        "CHROM": "chr2",
        "POS": 50000,
        "ID": "rs1122334455",
        "REF": "C",
        "ALT": "G",
    }
    del new_variant[missing_field]

    response = client_authed.post("/", data=new_variant)

    assert response.status_code == 400
    assert missing_field.lower() in response.json()
    assert_variant_not_in_file(new_variant)
