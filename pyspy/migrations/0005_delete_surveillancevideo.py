# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pyspy', '0004_auto_20150515_1104'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SurveillanceVideo',
        ),
    ]
