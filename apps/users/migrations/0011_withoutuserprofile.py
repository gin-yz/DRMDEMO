# Generated by Django 2.2.7 on 2020-04-11 01:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200410_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='WithoutUserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('address', models.CharField(default='', max_length=42, unique=True, verbose_name='账户地址')),
                ('is_producter', models.BooleanField(default=False, verbose_name='是否版权发布者')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
