# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-02 05:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0038_auto_20190202_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamcontent',
            name='publication_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
