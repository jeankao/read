# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-07 08:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0073_auto_20190207_1558'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseexercise',
            old_name='excise_id',
            new_name='exercise_id',
        ),
    ]