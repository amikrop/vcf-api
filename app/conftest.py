import shutil
from pathlib import Path

import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def use_default_settings():
    """Ensure default settings are used for tests."""
    settings.REST_FRAMEWORK["PAGE_SIZE"] = settings.DEFAULT_PAGE_SIZE
    settings.REST_FRAMEWORK["WRITE_TOKEN"] = settings.DEFAULT_WRITE_TOKEN


@pytest.fixture(autouse=True)
def temp_vcf_file(tmp_path):
    """Copy variants.vcf.test to a temporary file before each test
    and patch settings.VCF_FILE_PATH to point to it.
    """
    base_vcf = (Path(__file__).parent / "vcf" / "tests" / "variants.vcf.test").resolve()
    tmp_vcf = tmp_path / "variants.vcf"
    shutil.copy2(base_vcf, tmp_vcf)
    settings.VCF_FILE_PATH = str(tmp_vcf)


@pytest.fixture
def client_authed():
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {settings.WRITE_TOKEN}")
    return client
