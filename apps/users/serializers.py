from rest_framework import serializers
from django.contrib.auth.models import User
class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """
    username    = serializers.CharField()
    email       = serializers.EmailField()
    password    = serializers.CharField()

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance
    class Meta:
        model = User
        fields = ("id", "username","email","password")

