# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-27 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_auto_20170626_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfreply',
            name='work_id',
            field=models.IntegerField(default=0),
        ),
    ]
