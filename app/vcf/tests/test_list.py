def test_list_success(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "count": 8,
        "next": None,
        "previous": None,
        "results": [
            {
                "CHROM": "chr1",
                "POS": 10176,
                "ID": "rs367896724",
                "REF": "A",
                "ALT": "AC",
            },
            {
                "CHROM": "chr1",
                "POS": 10352,
                "ID": "rs555500075",
                "REF": "T",
                "ALT": "TA",
            },
            {
                "CHROM": "chr1",
                "POS": 10616,
                "ID": "rs540538026",
                "REF": "C",
                "ALT": "G",
            },
            {"CHROM": "chr1", "POS": 11008, "ID": "rs62635286", "REF": "C", "ALT": "G"},
            {
                "CHROM": "chr1",
                "POS": 13116,
                "ID": "rs201747181",
                "REF": "G",
                "ALT": "A",
            },
            {
                "CHROM": "chr2",
                "POS": 20000,
                "ID": "rs745120618",
                "REF": "T",
                "ALT": "C",
            },
            {"CHROM": "chr2", "POS": 20300, "ID": "rs62635287", "REF": "A", "ALT": "G"},
            {
                "CHROM": "chr3",
                "POS": 30000,
                "ID": "rs123456789",
                "REF": "G",
                "ALT": "T",
            },
        ],
    }


def test_list_xml(client):
    response = client.get("/", HTTP_ACCEPT="application/xml")
    content = response.content.decode("utf-8")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/xml")

    assert "<results>" in content
    assert "<CHROM>chr1</CHROM>" in content
    assert "<POS>10176</POS>" in content
    assert "<ID>rs367896724</ID>" in content


def test_list_pagination(client):
    response = client.get("/?limit=3&offset=2")

    assert response.status_code == 200
    assert response.json() == {
        "count": 8,
        "next": "http://testserver/?limit=3&offset=5",
        "previous": "http://testserver/?limit=3",
        "results": [
            {
                "CHROM": "chr1",
                "POS": 10616,
                "ID": "rs540538026",
                "REF": "C",
                "ALT": "G",
            },
            {"CHROM": "chr1", "POS": 11008, "ID": "rs62635286", "REF": "C", "ALT": "G"},
            {
                "CHROM": "chr1",
                "POS": 13116,
                "ID": "rs201747181",
                "REF": "G",
                "ALT": "A",
            },
        ],
    }


def test_list_etag(client):
    response1 = client.get("/?limit=2&offset=1")
    etag = response1["ETag"]

    response2 = client.get("/?limit=2&offset=1", HTTP_IF_NONE_MATCH=etag)

    assert response2.status_code == 304
    assert not response2.content
    assert "ETag" not in response2


def test_list_id_param(client):
    response = client.get("/?id=rs62635286")

    assert response.status_code == 200
    assert response.json() == {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
            {"CHROM": "chr1", "POS": 11008, "ID": "rs62635286", "REF": "C", "ALT": "G"}
        ],
    }


def test_list_id_param_not_found(client):
    response = client.get("/?id=rs00000000")

    assert response.status_code == 404
    assert response.json() == {"detail": "No records with id 'rs00000000' found."}
