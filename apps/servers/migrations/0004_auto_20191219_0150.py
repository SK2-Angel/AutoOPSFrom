# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-12-19 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0003_auto_20180701_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='rmt_card_ip',
            field=models.CharField(db_index=True, help_text='管理管理卡IP', max_length=15, null=True, verbose_name='管理管理卡IP'),
        ),
    ]