# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-05 00:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0008_auto_20170705_0422'),
    ]

    operations = [
        migrations.AddField(
            model_name='fclass',
            name='publication_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
