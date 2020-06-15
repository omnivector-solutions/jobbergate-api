from rest_framework import serializers

from apps.job_submissions.models import JobSubmission


class JobSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubmission
        fields = ['id', 'job_submission_name', 'job_submission_owner']

    def create(self, validated_data):
        job_script = JobSubmission.objects.create(**validated_data)
        return job_script
