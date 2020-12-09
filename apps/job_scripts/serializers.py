from rest_framework import serializers

from apps.job_scripts.models import JobScript


class JobScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobScript
        fields = [
            "id",
            "job_script_name",
            "job_script_description",
            "job_script_data_as_string",
            "job_script_owner",
            "application",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        job_script = JobScript.objects.create(**validated_data)
        return job_script
