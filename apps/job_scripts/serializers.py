from rest_framework import serializers

from apps.job_scripts.models import JobScript


class JobScriptSerializer(serializers.ModelSerializer):
    job_script_owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = JobScript
        fields = ['id', 'job_script_name', 'job_script_owner']

    def create(self, validated_data):
        job_script = JobScript.objects.create(**validated_data)
        return job_script
