from rest_framework import serializers

from apps.job_submissions.models import JobSubmission


class JobSubmissionSerializer(serializers.ModelSerializer):
    job_submission_owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = JobSubmission
        fields = ['id', 'job_submission_owner']

    def create(self, validated_data):
        job_submission = JobSubmission.objects.create(**validated_data)
        return job_submission


