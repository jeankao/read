# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-10-26 02:59
from __future__ import unicode_literals

from django.db import migrations, models
import teacher.models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0046_auto_20171026_0833'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_id', models.IntegerField(default=0)),
                ('qtype', models.IntegerField(default=0)),
                ('title', models.TextField(default=b'')),
                ('option1', models.CharField(blank=True, max_length=250, null=True)),
                ('option2', models.CharField(blank=True, max_length=250, null=True)),
                ('option3', models.CharField(blank=True, max_length=250, null=True)),
                ('option4', models.CharField(blank=True, max_length=250, null=True)),
                ('answer', models.IntegerField(default=0)),
                ('answer_text', models.TextField(default=b'')),
            ],
        ),
        migrations.AlterField(
            model_name='fclass',
            name='deadline_date',
            field=models.DateTimeField(default=teacher.models.get_deadline),
        ),
    ]
