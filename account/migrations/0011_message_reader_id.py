# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-08 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_auto_20170708_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reader_id',
            field=models.IntegerField(default=0),
        ),
    ]
