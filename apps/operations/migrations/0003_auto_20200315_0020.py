# Generated by Django 2.2.7 on 2020-03-15 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0002_musiccomments_userfavorite_usermessage_usermusic'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermusic',
            options={'verbose_name': '用户购买音乐', 'verbose_name_plural': '用户购买音乐'},
        ),
        migrations.AddField(
            model_name='usermusic',
            name='purchase_bcId',
            field=models.CharField(default='', max_length=32, verbose_name='购买凭证id'),
        ),
        migrations.AddField(
            model_name='usermusic',
            name='purchase_permission',
            field=models.IntegerField(default=0, verbose_name='购买的权限'),
        ),
        migrations.AddField(
            model_name='usermusic',
            name='purchase_transactionHash',
            field=models.CharField(default='', max_length=128, verbose_name='交易hash'),
        ),
    ]
