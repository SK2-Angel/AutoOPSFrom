# Generated by Django 2.0.5 on 2020-01-07 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('host_server', '0006_auto_20200107_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor_server_cpu_mem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(db_index=True, default='0.0.0.0', verbose_name='IP地址')),
                ('cpu_utilize', models.FloatField(db_index=True, default=0, verbose_name='CPU')),
                ('mem_utilize', models.FloatField(db_index=True, default=0, verbose_name='内存')),
                ('last_time', models.DateTimeField(db_index=True, verbose_name='检查时间')),
            ],
            options={
                'db_table': 'Monitor_cpus_mems',
                'ordering': ['id'],
            },
        ),
    ]
