# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-07 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0043_auto_20190203_0620'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examanswer',
            name='answer',
            field=models.TextField(default=b''),
        ),
    ]
