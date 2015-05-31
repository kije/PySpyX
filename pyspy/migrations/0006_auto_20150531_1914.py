# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pyspy', '0005_delete_surveillancevideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='ip',
            field=models.GenericIPAddressField(verbose_name='IP', unique=True, unpack_ipv4=True),
        ),
    ]
