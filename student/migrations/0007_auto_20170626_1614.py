# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-26 08:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0006_auto_20170626_1410'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sfreply',
            old_name='work_id',
            new_name='index',
        ),
    ]