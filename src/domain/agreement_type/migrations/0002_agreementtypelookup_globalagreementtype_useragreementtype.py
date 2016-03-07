# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agreement_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementTypeLookup',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(unique=True, max_length=2400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlobalAgreementType',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(unique=True, max_length=2400)),
                ('system_created_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAgreementType',
            fields=[
                ('primary_key', models.AutoField(primary_key=True, serialize=False)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('user_id', models.CharField(unique=True, max_length=8)),
                ('system_created_date', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
