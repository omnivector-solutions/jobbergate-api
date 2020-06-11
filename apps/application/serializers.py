from rest_framework import serializers

from apps.application.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    #job_script_owner = serializers.HiddenField(
    #    default=serializers.CurrentUserDefault()
    #)
    class Meta:
        model = Application
        fields = ['id', 'application_name', 'application_owner']

    def create(self, validated_data):
        job_script = Application.objects.create(**validated_data)
        return job_script
