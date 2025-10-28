import re

from rest_framework import serializers

from vcf.utils import write_vcf


class VCFSerializer(serializers.Serializer):
    chrom = serializers.CharField(max_length=6)
    pos = serializers.IntegerField(min_value=1)
    id = serializers.CharField(max_length=20)
    ref = serializers.CharField(max_length=1)
    alt = serializers.CharField(max_length=1)

    def validate_chrom(self, value):
        if not re.match(r"^chr(?:[1-9]|1\d|2[0-2]|X|Y|M)$", value):
            raise serializers.ValidationError(
                "CHROM must be prefixed with 'chr' followed by 1-22, 'X', 'Y', or 'M'."
            )
        return value

    def validate_id(self, value):
        if not re.match(r"^rs\d+$", value):
            raise serializers.ValidationError("ID must be in the form 'rs<integer>'.")
        return value

    def validate_ref(self, value):
        if value not in {"A", "C", "G", "T", "."}:
            raise serializers.ValidationError(
                "REF must be one of 'A', 'C', 'G', 'T', or '.'."
            )
        return value

    def validate_alt(self, value):
        if value not in {"A", "C", "G", "T", "."}:
            raise serializers.ValidationError(
                "ALT must be one of 'A', 'C', 'G', 'T', or '.'."
            )
        return value

    def to_representation(self, instance):
        # Convert output keys to uppercase
        rep = super().to_representation(instance)
        return {key.upper(): value for key, value in rep.items()}

    def to_internal_value(self, data):
        # Convert input keys to lowercase before validation
        lower_data = {k.lower(): v for k, v in data.items()}
        return super().to_internal_value(lower_data)

    def save(self):
        def process_record(record, outfile):
            # Just copy existing records
            outfile.write(record)

        # Rewrite VCF with a new record (from serializer data) added
        write_vcf(process_record, self.validated_data)
