from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, mixins
from .models import Server,NetworkDevice,IP
from .serilaizers import ServerAutoReportSerializer,NetworkDeviceSerializer,IPSerializer, ServerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ServerFilter


class ServerAutoReportViewset(mixins.CreateModelMixin,viewsets.GenericViewSet):
    """
    create:
        创建一个服务器
    """
    queryset = Server.objects.all()
    serializer_class = ServerAutoReportSerializer

class ServerViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
        列出所有服务器信息
    retrieve:
        读取一个服务器信息
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_class = ServerFilter
    filter_fields = ("hostname",)
    extra_perm_map = {
        "GET": ['servers.view_server']
    }


class NetworkDeviceViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
        列出所有网卡信息
    retrieve:
        读取一个网卡信息
    """
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer



class IPViewset(viewsets.ReadOnlyModelViewSet):
    """
    retrieve:
        返回一个ip信息
    list:
        列出所有IP信息
    """
    queryset = IP.objects.all()
    serializer_class = IPSerializer
