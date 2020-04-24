# Generated by Django 2.2.7 on 2020-03-12 00:40

import DjangoUeditor.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='image',
            field=models.ImageField(blank=True, upload_to='music/%Y/%m', verbose_name='封面图'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_demoLink',
            field=models.CharField(blank=True, max_length=64, verbose_name='ipfs试听音乐hash'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_desc',
            field=models.CharField(blank=True, max_length=300, verbose_name='歌曲描述'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_detail',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', verbose_name='歌曲详情'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_hashLink',
            field=models.CharField(blank=True, max_length=64, verbose_name='ipfshash'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='歌曲名'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_price1',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='个人价格'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_price2',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='版权价格1'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_price3',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='版权价格2'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_price4',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='版权价格3'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_price5',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='版权价格4'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_price6',
            field=models.CharField(blank=True, default='', max_length=128, verbose_name='版权价格5'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_times',
            field=models.IntegerField(blank=True, default=0, verbose_name='歌曲时长(分钟数)'),
        ),
        migrations.AlterField(
            model_name='music',
            name='music_transactionHash',
            field=models.CharField(blank=True, max_length=128, verbose_name='交易hash'),
        ),
    ]
