from django.conf import settings
from pysam import VariantFile

from vcf.utils import record_to_dict


def record_to_data(record):
    record_dict = record_to_dict(record)
    return {key.upper(): value for key, value in record_dict.items()}


def assert_variant_not_in_file(variant):
    with VariantFile(settings.VCF_FILE_PATH) as infile:
        for rec in infile.fetch():
            assert record_to_data(rec) != variant
