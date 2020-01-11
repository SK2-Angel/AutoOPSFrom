from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import datetime
from time import strftime,gmtime

class Host_server(models.Model):
    purpose = models.CharField("用处",max_length=512,default='')
    hostname = models.CharField("主机名",max_length=32,default='')
    ip   = models.GenericIPAddressField("IP地址",null=False,default='0.0.0.0',db_index=True, unique=True,)
    mac  = models.CharField("MAC地址",max_length=32,null=False,default='00:00:00:00:00:00')
    os   = models.CharField("操作系统",max_length=32,default='')
    mem  = models.BigIntegerField("内存",null=False, default=0)
    cpu  = models.IntegerField("CPU",null=False, default=0)
    disk = models.CharField("硬盘",max_length=512,null=False,default='{}')
    sn   = models.CharField("服务器型号",max_length=128,null=False,default='')
    remark = models.TextField("备注",null=False, default='')
    create_time = models.DateTimeField("创建时间",null=False, auto_now_add=True)
    last_time = models.DateTimeField("最后一次检查时间",null=False)
    def __str__(self):
        return self.model_name

    class Meta:
        db_table = "Host_server"
        ordering = ["id"]

    @classmethod
    def Host_server_insert_data(cls,hostname,ip,mac,os,mem,cpu,disk,sn):
        date_time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        obj = None
        try:
            obj = cls.objects.get(ip=ip)
        except ObjectDoesNotExist as e:
            obj = cls()
            obj.ip = ip
        obj.hostname = hostname
        obj.mac = mac
        obj.os = os
        obj.mem = mem
        obj.cpu = cpu
        obj.disk = disk
        obj.sn = sn
        obj.last_time = date_time
        obj.save()

class Host_server_status(models.Model):
    ip = models.GenericIPAddressField("IP地址", null=False, default='0.0.0.0', db_index=True, unique=True, )
    status = models.CharField("服务器状态",max_length=32,null=False,default='0')
    Damage_times = models.IntegerField("故障次数",null=False, default=0)
    create_time = models.DateTimeField("创建时间",null=False, auto_now_add=True)
    last_time = models.DateTimeField("最后一次检查时间",null=False)
    def __str__(self):
        return self.model_name

    class Meta:
        db_table = "Host_server_status"
        ordering = ["id"]


class Host_server_cpu_mem(models.Model):
    ip = models.GenericIPAddressField("IP地址", null=False, default='0.0.0.0', db_index=True,unique=True)
    cpu_utilize = models.FloatField("CPU",null=False, default=0,db_index=True)
    mem_utilize= models.FloatField("内存", null=False, default=0,db_index=True)
    create_time = models.DateTimeField("创建时间", null=False, auto_now_add=True)
    last_time = models.DateTimeField("最后一次检查时间", null=False,db_index=True)
    disk_utilize = models.CharField("硬盘", max_length=512, null=False, default='{}')
    def __str__(self):
        return self.model_name

    class Meta:
        db_table = "Host_server_cpu_mem"
        ordering = ["id"]
    @classmethod
    def Host_server_cpu_mem_insert(cls,ip,cpu,mem,disk):
        date_time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        obj = None
        try:
            obj = cls.objects.get(ip=ip)
        except ObjectDoesNotExist as e:
            obj = cls()
            obj.ip = ip
        obj.mem_utilize = mem
        obj.cpu_utilize = cpu
        obj.disk_utilize = disk
        obj.last_time = date_time
        obj.save()


class Monitor_server_cpu_mem(models.Model):
    ip = models.GenericIPAddressField("IP地址", null=False, default='0.0.0.0', db_index=True,)
    cpu_utilize = models.FloatField("CPU", null=False, default=0, db_index=True)
    mem_utilize = models.FloatField("内存", null=False, default=0, db_index=True)
    last_time = models.DateTimeField("检查时间", null=False, db_index=True)
    def __str__(self):
        return self.model_name

    class Meta:
        db_table = "Monitor_cpus_mems"
        ordering = ["id"]

    @classmethod

    def Monitor_server_cpu_mem_insert(cls,ip,cpu,mem,):
        date_time = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        obj = None
        obj = cls()
        obj.ip = ip
        obj.mem_utilize = mem
        obj.cpu_utilize = cpu
        obj.last_time = date_time
        obj.save()