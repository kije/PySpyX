# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
