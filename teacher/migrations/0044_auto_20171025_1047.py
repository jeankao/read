# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-25 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0043_auto_20171025_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]
