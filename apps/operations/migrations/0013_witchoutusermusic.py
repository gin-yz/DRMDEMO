# Generated by Django 2.2.7 on 2020-04-10 14:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0012_auto_20200409_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='WitchoutUserMusic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('purchase_bcId', models.CharField(default='', max_length=32, verbose_name='购买凭证id')),
                ('purchase_transactionHash', models.CharField(default='', max_length=128, verbose_name='交易hash')),
                ('purchase_permission', models.IntegerField(default=0, verbose_name='购买的权限')),
                ('purchase_isUpdate', models.IntegerField(default=0, verbose_name='是否升级')),
                ('music_price', models.CharField(default='', max_length=128, verbose_name='价格')),
                ('timestamp', models.CharField(default='', max_length=128, verbose_name='上链时间戳')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
