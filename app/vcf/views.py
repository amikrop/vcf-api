import hashlib
import os

from django.conf import settings
from pysam import VariantFile
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from vcf.permissions import IsAuthorizedOrReadOnly
from vcf.serializers import VCFSerializer
from vcf.utils import make_record, record_to_dict, write_vcf


class VCFView(generics.ListCreateAPIView):
    """List, create, update, and delete VCF records."""

    serializer_class = VCFSerializer
    permission_classes = [IsAuthorizedOrReadOnly]

    def get_queryset(self):
        id = self.request.query_params.get("id")

        records = []
        with VariantFile(settings.VCF_FILE_PATH) as infile:
            for rec in infile.fetch():
                if id is None or rec.id == id:
                    records.append(record_to_dict(rec))

        if id is not None and not records:
            raise NotFound(f"No records with id '{id}' found.")

        return records

    def list(self, request):
        # Compute ETag based on file mtime + optional query params
        record_id = request.query_params.get("id", "")
        limit = request.query_params.get("limit", "")
        offset = request.query_params.get("offset", "")
        vcf_mtime = os.path.getmtime(settings.VCF_FILE_PATH)

        etag_raw = f"{vcf_mtime}-{record_id}-{limit}-{offset}"
        etag = hashlib.sha1(etag_raw.encode()).hexdigest()

        # Check If-None-Match header
        if_none_match = request.headers.get("If-None-Match")
        if if_none_match == etag:
            return Response(status=304)

        response = super().list(request)

        # Add ETag header and return response
        response["ETag"] = etag
        return response

    def _modify(self, process_record):
        self.record_id = self.request.query_params.get("id")
        if not self.record_id:
            raise NotFound("Query parameter 'id' is required.")

        is_modified = write_vcf(process_record)

        if not is_modified:
            raise NotFound(f"No records with id '{self.record_id}' found.")

    def put(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        def process_record(record, outfile):
            if record.id == self.record_id:
                # Replace matching record
                new_record = make_record(data, outfile)
                outfile.write(new_record)
                return True  # Indicate update
            else:
                # Keep other records unchanged
                outfile.write(record)

        self._modify(process_record)

        return Response(serializer.data)

    def delete(self, request):
        def process_record(record, outfile):
            if record.id != self.record_id:
                # Keep records that don't match the ID
                outfile.write(record)
            else:
                return True  # Indicate deletion

        self._modify(process_record)

        return Response(status=status.HTTP_204_NO_CONTENT)
