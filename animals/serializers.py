from characteristics.models import Characteristic
from characteristics.serializers import CharacteristicSerializer
from groups.models import Group
from groups.serializers import GroupSerializer
from rest_framework import serializers

from .models import Animal


class AnimalSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    age = serializers.FloatField()
    weight = serializers.FloatField()
    sex = serializers.CharField()
    group = GroupSerializer()
    characteristics = CharacteristicSerializer(many=True)

    def create(self, validated_data):

        validated_group = validated_data.pop("group")
        validated_charac = validated_data.pop("characteristics")

        group, _ = Group.objects.get_or_create(**validated_group)
        animal = Animal.objects.create(**validated_data, group=group)

        for char in validated_charac:
            charac, _ = Characteristic.objects.get_or_create(**char)
            animal.characteristics.add(charac)

        return animal

    def update(self, instance: Animal, validated_data: dict):
        non_editable_keys = (
            "sex",
            "group",
        )

        for key in non_editable_keys:
            if key in validated_data:
                raise KeyError(f"you can not update {key} property")

        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.weight = validated_data.get("weight", instance.weight)

        instance.save()

        return instance
