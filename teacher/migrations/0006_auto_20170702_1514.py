# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-02 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0005_assistant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='group_open',
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='group_size',
        ),
        migrations.AddField(
            model_name='classroom',
            name='domains',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='classroom',
            name='levels',
            field=models.TextField(default=b''),
        ),
    ]
