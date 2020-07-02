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
        print(validated_data['job_script'])
        job_script_id = validated_data['job_script'].id
        print(job_script_id)
        # job_script =
        # application_id =
        return job_submission
