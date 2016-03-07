# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgreementAlert',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('expiration_alert_date', models.DateTimeField(blank=True, null=True)),
                ('expiration_alert_enabled', models.BooleanField()),
                ('expiration_alert_created', models.BooleanField()),
                ('outcome_notice_alert_date', models.DateTimeField(blank=True, null=True)),
                ('outcome_notice_alert_enabled', models.BooleanField()),
                ('outcome_notice_alert_created', models.BooleanField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgreementSearch',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('user_id', models.CharField(max_length=8)),
                ('counterparty', models.CharField(max_length=2400, null=True, blank=True)),
                ('agreement_type_id', models.CharField(max_length=8, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
