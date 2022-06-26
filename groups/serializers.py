from rest_framework import serializers
from .models import Group

class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    scientific_name = serializers.CharField()
    

    def create(self, validated_data):
        return Group.objects.create(**validated_data)


