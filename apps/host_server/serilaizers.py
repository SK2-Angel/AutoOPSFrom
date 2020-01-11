from rest_framework import serializers
from .models import Host_server,Host_server_status,Host_server_cpu_mem,Monitor_server_cpu_mem

class Host_server_serializers(serializers.ModelSerializer):

    class Meta:
        model = Host_server
        fields = "__all__"

class Host_server_statuSerializers(serializers.ModelSerializer):

    class Meta:
        model = Host_server_status
        fields = "__all__"

class Host_server_cpu_memSerializers(serializers.ModelSerializer):

    class Meta:
        model = Host_server_cpu_mem
        fields = "__all__"
class Monitor_server_cpu_memSerializers(serializers.ModelSerializer):

    class Meta:
        model =  Monitor_server_cpu_mem
        fields = "__all__"
