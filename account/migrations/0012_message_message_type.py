# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-07-08 08:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_message_reader_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.IntegerField(default=0),
        ),
    ]