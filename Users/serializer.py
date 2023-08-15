from rest_framework import serializers
from .models import UserInfo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"

    def create(self, validated_data):
        user = UserInfo.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get("firstname", instance.firstname)
        instance.lastname = validated_data.get("lastname", instance.firstname)
        instance.password = validated_data.get("password", instance.password)
        instance.gmail = validated_data.get("email", instance.email)
        instance.phone = validated_data.get("phone", instance.phone)

        instance.save()
        return instance
