# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-02 05:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0040_auto_20190202_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teamcontent',
            old_name='enroll_id',
            new_name='user_id',
        ),
    ]