# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-27 04:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0033_auto_20171027_1204'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examanswer',
            old_name='exam_work_id',
            new_name='examwork_id',
        ),
        migrations.AlterUniqueTogether(
            name='examanswer',
            unique_together=set([('student_id', 'examwork_id', 'question_id')]),
        ),
    ]