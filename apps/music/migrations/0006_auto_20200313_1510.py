# Generated by Django 2.2.7 on 2020-03-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0005_auto_20200313_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musictag',
            name='tag',
            field=models.IntegerField(max_length=100, verbose_name='标签'),
        ),
    ]
