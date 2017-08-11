# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-08-11 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_auto_20170811_0751'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='speculationcontent',
            name='link',
        ),
        migrations.AddField(
            model_name='speculationcontent',
            name='text',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]
