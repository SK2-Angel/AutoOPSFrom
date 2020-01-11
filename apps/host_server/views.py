from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Host_server,Host_server_status,Host_server_cpu_mem,Monitor_server_cpu_mem
from .serilaizers import Host_server_serializers,Host_server_statuSerializers,Host_server_cpu_memSerializers
from rest_framework import filters
from .baseviews import BaseView
import datetime
from datetime import  timedelta
from time import strftime,gmtime
import json
class Host_server_Viewset(viewsets.ModelViewSet):
    queryset = Host_server.objects.all()
    serializer_class = Host_server_serializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['hostname','ip','mac','sn']

class Host_server_statsuViewset(viewsets.ModelViewSet):
    queryset = Host_server_status.objects.all()
    serializer_class = Host_server_statuSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['ip']
class Host_server_cpu_memViewset(viewsets.ModelViewSet):
    queryset = Host_server_cpu_mem.objects.all()
    serializer_class = Host_server_cpu_memSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['ip']




class Hoser_cpus_memsViewst(BaseView):
    def create(self, request, *args, **kwargs):
        date_time_day1 = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        ip=request.data.get('ip')
        select_server_cpu_mem=Monitor_server_cpu_mem.objects.filter(ip=ip,last_time__gte=date_time_day1).order_by('last_time')
        cpus=[]
        mems=[]
        datetimes=[]
        for rest in select_server_cpu_mem:
            cpus.append(rest.cpu_utilize)
            mems.append(rest.mem_utilize)
            datetimes.append(rest.last_time)
        date_dict={}
        date_dict['ip']=ip
        date_dict['cpus']=cpus
        date_dict['mem'] = mems
        date_dict['datetimes']=datetimes
        return Response(date_dict)













# class Host_disk_listViewset(BaseView):
#     def create(self,request,*args,**kwargs):
#         request_ip=request.data.get('ip')
#         host_server_object=Host_server_cpu_mem.objects.get(ip=request_ip)
#         disk_data = eval(host_server_object.disk_utilize)
#         disk_temp=disk_data.get('disk')
#
#         disk={}
#         for datas in disk_temp:
#             if datas != '':
#                 disk=dict()
#                 temps = datas.split()
#                 disk['disk_name']=temps[2]
#                 disk['size']=temps[3]
#                 disk['Percentage']=temps[4]
#             else:
#                 break
#         print(disk)
#         return Response('aa')
