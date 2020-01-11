#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from utils.basemodels import Basemodel
# Create your models here.

class Dbconf(Basemodel):
    GENDER_CHOICES = (
        ('prd', u'生产环境'),
        ('test', u'测试环境')
    )
    user = models.CharField(max_length = 128)
    password = models.CharField(max_length = 128)
    host = models.CharField(max_length = 16)
    port = models.CharField(max_length = 5)
    env = models.CharField(max_length = 20, choices = GENDER_CHOICES)
    sql_content = models.TextField(default=None)

class DB_change(models.Model):
    createtime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updatetime = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    db_user = models.CharField(max_length=128,verbose_name='用户')
    db_password = models.CharField(max_length=128,verbose_name='密码')
    host = models.CharField(max_length = 16,verbose_name='数据库地址')
    port = models.CharField(max_length = 5,verbose_name='端口号')
    remark = models.TextField(default='', null=True, blank=True, verbose_name='备注')
    def __str__(self):
        return self.model_name

    class Meta:
        db_table = "db_change"
        ordering = ["id"]
