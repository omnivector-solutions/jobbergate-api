from rest_framework import serializers

from apps.applications.models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    #job_script_owner = serializers.HiddenField(
    #    default=serializers.CurrentUserDefault()
    #)
    class Meta:
        model = Application
        fields = [
            'id',
            'application_name',
            'application_description',
            'application_location',
            'application_dir_listing',
            'application_dir_listing_acquired',
            'application_owner',
            'application_file',
            'created_at',
            'updated_at'
        ]

    def create(self, validated_data):
        application = Application.objects.create(**validated_data)
        return application
