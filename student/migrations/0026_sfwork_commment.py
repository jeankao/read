# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-24 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0025_studentgroup_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfwork',
            name='commment',
            field=models.TextField(default=b''),
        ),
    ]