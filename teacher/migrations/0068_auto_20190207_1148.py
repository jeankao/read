# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-07 03:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0067_auto_20190207_1124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examquestion',
            old_name='answer_text',
            new_name='answer_assay',
        ),
        migrations.AddField(
            model_name='examquestion',
            name='answer_filling',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='examquestion',
            name='filename',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='examquestion',
            name='pic',
            field=models.FileField(blank=True, null=True, upload_to=b''),
        ),
    ]
