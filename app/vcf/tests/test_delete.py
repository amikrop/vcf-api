from django.conf import settings
from pysam import VariantFile


def test_delete_success(client_authed):
    response = client_authed.delete("/?id=rs555500075")

    with VariantFile(settings.VCF_FILE_PATH) as infile:
        ids_in_file = [rec.id for rec in infile.fetch()]

    assert response.status_code == 204
    assert "rs555500075" not in ids_in_file


def test_delete_missing_id_param(client_authed):
    response = client_authed.delete("/")

    assert response.status_code == 404
    assert response.json() == {"detail": "Query parameter 'id' is required."}


def test_delete_not_found(client_authed):
    response = client_authed.delete("/?id=rs000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "No records with id 'rs000000' found."}


def test_delete_unauthorized(client):
    response = client.delete("/?id=rs367896724")

    with VariantFile(settings.VCF_FILE_PATH) as infile:
        ids_in_file = [rec.id for rec in infile.fetch()]

    assert response.status_code == 403
    assert "rs367896724" in ids_in_file
