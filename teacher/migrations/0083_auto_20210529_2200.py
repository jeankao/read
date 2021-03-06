# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2021-05-29 14:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0082_exam_opening'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='domains',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='classroom',
            name='levels',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='coursecontent',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='coursecontent',
            name='memo',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='coursework',
            name='domains',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='coursework',
            name='levels',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='coursework',
            name='title',
            field=models.CharField(max_length=250, verbose_name='課程主題'),
        ),
        migrations.AlterField(
            model_name='exam',
            name='domains',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='exam',
            name='levels',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='exam',
            name='title',
            field=models.CharField(max_length=250, verbose_name='測驗主題'),
        ),
        migrations.AlterField(
            model_name='examimportquestion',
            name='answer',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='examimportquestion',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='examquestion',
            name='answer',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='examquestion',
            name='title',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='examquestion',
            name='title_pic',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='fcontent',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='fcontent',
            name='memo',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='fwork',
            name='domains',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='fwork',
            name='levels',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='fwork',
            name='title',
            field=models.CharField(max_length=250, verbose_name='討論主題'),
        ),
        migrations.AlterField(
            model_name='speculationcontent',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='speculationcontent',
            name='memo',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='speculationcontent',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='speculationwork',
            name='domains',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='speculationwork',
            name='levels',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='speculationwork',
            name='title',
            field=models.CharField(max_length=250, verbose_name='思辨主題'),
        ),
        migrations.AlterField(
            model_name='teamcontent',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='teamcontent',
            name='memo',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='teamwork',
            name='domains',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='teamwork',
            name='levels',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='teamwork',
            name='title',
            field=models.CharField(max_length=250, verbose_name='任務主題'),
        ),
    ]
