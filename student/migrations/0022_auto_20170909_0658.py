# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-09-08 22:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_auto_20170824_0715'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfwork',
            name='memo_c',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sfwork',
            name='memo_e',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
