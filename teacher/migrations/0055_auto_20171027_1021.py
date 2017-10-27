# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-27 02:21
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0054_auto_20171027_1017'),
    ]

    operations = [
        migrations.AddField(
            model_name='examimportquestion2',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]
