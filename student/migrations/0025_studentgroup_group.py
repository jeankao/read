# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-14 03:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0024_auto_20171014_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentgroup',
            name='group',
            field=models.IntegerField(default=0),
        ),
    ]
