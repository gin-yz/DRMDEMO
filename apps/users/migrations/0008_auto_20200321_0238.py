# Generated by Django 2.2.7 on 2020-03-21 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_userprofile_is_producter'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default='', max_length=50, verbose_name='个人描述'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='points',
            field=models.CharField(default='', max_length=20, verbose_name='作曲风格'),
        ),
    ]
