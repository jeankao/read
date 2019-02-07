# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2019-02-07 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0080_auto_20190208_0319'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamImportQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(default=b'')),
                ('option1', models.CharField(blank=True, max_length=250, null=True)),
                ('option2', models.CharField(blank=True, max_length=250, null=True)),
                ('option3', models.CharField(blank=True, max_length=250, null=True)),
                ('option4', models.CharField(blank=True, max_length=250, null=True)),
                ('answer', models.TextField(default=b'')),
                ('score', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='ExamImportQuestion1',
        ),
        migrations.DeleteModel(
            name='ExamImportQuestion2',
        ),
        migrations.DeleteModel(
            name='ExamImportQuestion3',
        ),
    ]
