import os
import shutil
import tempfile

from django.conf import settings
from pysam import VariantFile


def record_to_dict(record):
    return {
        "chrom": record.contig,
        "pos": record.pos,
        "id": record.id,
        "ref": record.ref,
        "alt": record.alts[0] if record.alts else "",
    }


def make_record(data, outfile):
    return outfile.new_record(
        contig=data["chrom"],
        start=data["pos"] - 1,  # pysam uses 0-based start
        stop=data["pos"],
        id=data["id"],
        alleles=[data["ref"], data["alt"]],
    )


def write_vcf(process_record, new_data=None):
    """Rewrite VCF file, processing each record with the process_record function.
    Return True if any records were modified, False otherwise.
    """
    # Open existing VCF file
    infile = VariantFile(settings.VCF_FILE_PATH)
    header = infile.header

    # Temporary file for safe rewriting
    fd, tmp_path = tempfile.mkstemp(suffix=".vcf")
    os.close(fd)

    is_modified = False
    with VariantFile(tmp_path, "w", header=header) as outfile:
        # Process existing records
        for record in infile.fetch():
            modifies_record = process_record(record, outfile)
            if modifies_record:
                is_modified = True

        # Optionally add new record
        if new_data is not None:
            new_record = make_record(new_data, outfile)
            outfile.write(new_record)

    infile.close()

    # Replace the original VCF file
    shutil.copyfile(tmp_path, settings.VCF_FILE_PATH)
    os.remove(tmp_path)

    return is_modified
