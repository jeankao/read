# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-25 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0048_auto_20190209_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='examanswer',
            name='answer_right',
            field=models.BooleanField(default=False),
        ),
    ]
