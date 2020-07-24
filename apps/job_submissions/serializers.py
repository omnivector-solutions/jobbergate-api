from rest_framework import serializers

from apps.job_submissions.models import JobSubmission


class JobSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSubmission
        fields = [
            'id',
            'job_submission_name',
            'job_submission_description',
            'job_submission_owner',
            'job_script',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        job_submission = JobSubmission.objects.create(**validated_data)
        return job_submission
