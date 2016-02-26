# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalAgreementType',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('version', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=2400, unique=True)),
                ('system_created_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAgreementType',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(max_length=8, unique=True)),
                ('version', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('name', models.CharField(max_length=2400)),
                ('user_id', models.CharField(max_length=8, unique=True)),
                ('system_created_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
