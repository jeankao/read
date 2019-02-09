# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-09 09:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0046_auto_20190209_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecontentprogress',
            name='end_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coursecontentprogress',
            name='start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
