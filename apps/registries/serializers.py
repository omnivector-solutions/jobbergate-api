from rest_framework import serializers

from apps.registries.models import Registry


class RegistrySerializer(serializers.ModelSerializer):
    registry_owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Registry
        fields = ['id', 'registry_owner']

    def create(self, validated_data):
        registry = Registry.objects.create(**validated_data)
        return registry
