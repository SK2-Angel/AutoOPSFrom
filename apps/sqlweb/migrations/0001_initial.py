# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-12-23 08:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dbconf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='名字')),
                ('createtime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updatetime', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('remark', models.TextField(blank=True, default='', null=True, verbose_name='备注')),
                ('user', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('host', models.CharField(max_length=16)),
                ('port', models.CharField(max_length=5)),
                ('env', models.CharField(choices=[('prd', '生产环境'), ('test', '测试环境')], max_length=20)),
            ],
            options={
                'ordering': ['-id'],
                'abstract': False,
            },
        ),
    ]
