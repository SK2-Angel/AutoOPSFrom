from django.contrib.auth.models import Group,Permission
from rest_framework import serializers

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "name")


class permissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ("id", "name","codename")
