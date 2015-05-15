# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pyspy', '0003_surveillancevideos'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveillanceVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='',
                                        verbose_name='ID')),
                ('date', models.DateTimeField(help_text='', verbose_name='Capture Date', auto_now_add=True)),
                ('path', models.CharField(help_text='', max_length=512, verbose_name='Path')),
                ('last_modified',
                 models.DateTimeField(auto_now=True, help_text='', null=True, verbose_name='Last modified')),
            ],
        ),
        migrations.DeleteModel(
            name='SurveillanceVideos',
        ),
        migrations.AddField(
            model_name='camera',
            name='last_modified',
            field=models.DateTimeField(auto_now=True, help_text='', null=True, verbose_name='Last modified'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='name',
            field=models.CharField(help_text='', max_length=150, null=True, verbose_name='Name', blank=True),
        ),
    ]
