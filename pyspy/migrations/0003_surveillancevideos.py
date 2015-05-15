# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pyspy', '0002_auto_20150505_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveillanceVideos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, help_text='',
                                        verbose_name='ID')),
            ],
        ),
    ]
