# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-23 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0021_auto_20170823_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='speculationcontent',
            name='link',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]
