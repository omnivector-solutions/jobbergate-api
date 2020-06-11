from rest_framework import serializers

from apps.job_submission.models import JobSubmission


class JobSubmissionSerializer(serializers.ModelSerializer):
    #job_script_owner = serializers.HiddenField(
    #    default=serializers.CurrentUserDefault()
    #)
    class Meta:
        model = JobSubmission
        fields = ['id', 'job_submission_name', 'job_submission_owner']

    def create(self, validated_data):
        job_script = JobSubmission.objects.create(**validated_data)
        return job_script
