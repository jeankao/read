# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-02 06:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0041_auto_20190202_1355'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamcontent',
            name='publish',
            field=models.BooleanField(default=False),
        ),
    ]
