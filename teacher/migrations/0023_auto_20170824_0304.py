# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-23 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0022_auto_20170823_1754'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
        migrations.AlterField(
            model_name='fcontent',
            name='filename',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='speculationcontent',
            name='filename',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
