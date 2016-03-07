# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AssetLookup',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('path', models.CharField(max_length=2400)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
