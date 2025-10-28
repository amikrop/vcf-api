import pytest
from django.conf import settings
from pysam import VariantFile

from vcf.tests.utils import assert_variant_not_in_file, record_to_data


def _get_record_by_id(record_id):
    with VariantFile(settings.VCF_FILE_PATH) as infile:
        for record in infile.fetch():
            if record.id == record_id:
                return record


def test_update_success(client_authed):
    updated_variant = {
        "CHROM": "chr2",
        "POS": 10176,
        "ID": "rs367896724",
        "REF": "T",
        "ALT": "G",
    }
    response = client_authed.put("/?id=rs367896724", data=updated_variant)
    updated_record = _get_record_by_id("rs367896724")

    assert response.status_code == 200
    assert response.json() == updated_variant
    assert record_to_data(updated_record) == updated_variant


def test_update_missing_id_param(client_authed):
    updated_variant = {
        "CHROM": "chr2",
        "POS": 10100,
        "ID": "rs555500075",
        "REF": "T",
        "ALT": "G",
    }
    response = client_authed.put("/", data=updated_variant)

    assert response.status_code == 404
    assert response.json() == {"detail": "Query parameter 'id' is required."}


def test_update_not_found(client_authed):
    updated_variant = {
        "CHROM": "chr2",
        "POS": 15300,
        "ID": "rs999999",
        "REF": "A",
        "ALT": "C",
    }
    response = client_authed.put("/?id=rs999999", data=updated_variant)

    assert response.status_code == 404
    assert response.json() == {"detail": "No records with id 'rs999999' found."}


def test_update_unauthorized(settings, client):
    updated_variant = {
        "CHROM": "chr1",
        "POS": 10176,
        "ID": "rs367896724",
        "REF": "G",
        "ALT": "A",
    }
    response = client.put("/?id=rs367896724", data=updated_variant)
    original_record = _get_record_by_id("rs367896724")

    assert response.status_code == 403
    assert record_to_data(original_record) != updated_variant


def test_update_invalid_data(client_authed):
    invalid_variant = {
        "CHROM": "chr2",
        "POS": 0,
        "ID": "invalid_id",
        "REF": "X",
        "ALT": "Y",
    }
    response = client_authed.put("/?id=rs367896724", data=invalid_variant)

    assert response.status_code == 400
    assert response.json() == {
        "pos": ["Ensure this value is greater than or equal to 1."],
        "id": ["ID must be in the form 'rs<integer>'."],
        "ref": ["REF must be one of 'A', 'C', 'G', 'T', or '.'."],
        "alt": ["ALT must be one of 'A', 'C', 'G', 'T', or '.'."],
    }
    assert_variant_not_in_file(invalid_variant)


@pytest.mark.parametrize("missing_field", ["CHROM", "POS", "ID", "REF", "ALT"])
def test_update_missing_field(client_authed, missing_field):
    updated_variant = {
        "CHROM": "chr2",
        "POS": 10176,
        "ID": "rs745120618",
        "REF": "T",
        "ALT": "G",
    }
    del updated_variant[missing_field]

    response = client_authed.put("/?id=rs745120618", data=updated_variant)

    assert response.status_code == 400
    assert missing_field.lower() in response.json()
    assert_variant_not_in_file(updated_variant)
