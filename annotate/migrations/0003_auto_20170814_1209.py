# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-14 04:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('annotate', '0002_auto_20170808_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='atype',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='annotation',
            name='ftype',
            field=models.IntegerField(default=0),
        ),
    ]
