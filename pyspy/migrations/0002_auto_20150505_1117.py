# -*- coding: utf-8 -*-
from __future__ import unicode_literals

"""
Camera Surveillance tool for Raspberry Pi with Camera module Project in ICT M152.
Copyright (C) 2015  Kim D. Jeker

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = 'kije'

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
