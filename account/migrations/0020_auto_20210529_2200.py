# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2021-05-29 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_auto_20171111_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='領域名稱'),
        ),
        migrations.AlterField(
            model_name='importuser',
            name='email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='importuser',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='importuser',
            name='password',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='importuser',
            name='username',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='level',
            name='title',
            field=models.CharField(default='', max_length=200, verbose_name='年級'),
        ),
        migrations.AlterField(
            model_name='message',
            name='content',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='visitorlog',
            name='IP',
            field=models.CharField(default='', max_length=20),
        ),
    ]
