# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('version', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('system_created_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
