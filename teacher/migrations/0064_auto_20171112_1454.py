# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-11-12 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0063_auto_20171111_1630'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamclass',
            name='group',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='examclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
        migrations.AlterField(
            model_name='speculationclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
        migrations.AlterUniqueTogether(
            name='teamclass',
            unique_together=set([('team_id', 'classroom_id')]),
        ),
    ]
