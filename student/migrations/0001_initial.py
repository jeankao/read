# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-23 23:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Assistant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('lesson', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Enroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('seat', models.IntegerField(default=0)),
                ('group', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EnrollGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('classroom_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SFWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(default=0)),
                ('index', models.IntegerField()),
                ('memo', models.TextField(default=b'')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('score', models.IntegerField(default=-1)),
                ('scorer', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField(default=0)),
                ('index', models.IntegerField()),
                ('youtube', models.CharField(max_length=100)),
                ('memo', models.TextField(default=b'')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('score', models.IntegerField(default=-1)),
                ('scorer', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='enroll',
            unique_together=set([('student_id', 'classroom_id')]),
        ),
    ]
