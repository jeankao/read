# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-14 05:51
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0038_auto_20171014_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='speculationclass',
            name='group',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]