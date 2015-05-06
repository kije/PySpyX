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
    ]

    operations = [
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(unpack_ipv4=True)),
                ('name', models.CharField(null=True, max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
