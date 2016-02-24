# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.libs.common_domain.aggregate_base
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('agreement_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('artifacts', jsonfield.fields.JSONField(default=list)),
                ('counterparty', models.CharField(max_length=2400)),
                ('description', models.TextField(null=True, blank=True)),
                ('execution_date', models.DateTimeField()),
                ('outcome_date', models.DateTimeField(null=True, blank=True)),
                ('term_length_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('term_length_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('auto_renew', models.BooleanField()),
                ('outcome_notice_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('outcome_notice_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('outcome_notice_date', models.DateTimeField(null=True, blank=True)),
                ('outcome_notice_alert_enabled', models.BooleanField()),
                ('outcome_notice_alert_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('outcome_notice_alert_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('outcome_notice_alert_created', models.BooleanField()),
                ('outcome_notice_alert_expired', models.BooleanField()),
                ('outcome_notice_alert_date', models.DateTimeField(null=True, blank=True)),
                ('expiration_alert_enabled', models.BooleanField()),
                ('expiration_alert_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('expiration_alert_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('expiration_alert_created', models.BooleanField()),
                ('expiration_alert_expired', models.BooleanField()),
                ('expiration_alert_date', models.DateTimeField(null=True, blank=True)),
                ('duration_details', models.TextField(null=True, blank=True)),
                ('system_created_date', models.DateTimeField()),
                ('agreement_type', models.ForeignKey(related_name='agreements', null=True, to_field='id', to='agreement_type.AgreementType', blank=True)),
                ('user', models.ForeignKey(to='user.User', to_field='id', related_name='agreements')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
