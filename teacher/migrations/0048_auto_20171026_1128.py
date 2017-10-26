# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-26 03:28
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0047_auto_20171026_1059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examquestion',
            old_name='qtype',
            new_name='types',
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]
