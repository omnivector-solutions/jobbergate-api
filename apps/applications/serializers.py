from rest_framework import serializers

from apps.applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = [
            'id',
            'application_name',
            'application_description',
            'application_location',
            'application_owner',
            'application_file',
            'application_config',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        application = Application.objects.create(**validated_data)
        return application
