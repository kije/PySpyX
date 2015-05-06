# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('pyspy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='ip',
            field=models.GenericIPAddressField(verbose_name='IP', unpack_ipv4=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='camera',
            name='name',
            field=models.CharField(null=True, verbose_name='Name', max_length=150),
            preserve_default=True,
        ),
    ]
