# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
        ('agreement_type', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('potential_agreement_id', models.CharField(unique=True, max_length=8)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('potential_agreement_artifacts', jsonfield.fields.JSONField(default=list)),
                ('potential_agreement_counterparty', models.CharField(null=True, blank=True, max_length=2400)),
                ('potential_agreement_description', models.TextField(null=True, blank=True)),
                ('potential_agreement_execution_date', models.DateTimeField(null=True, blank=True)),
                ('potential_agreement_outcome_date', models.DateTimeField(null=True, blank=True)),
                ('potential_agreement_term_length_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_term_length_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_auto_renew', models.NullBooleanField()),
                ('potential_agreement_outcome_notice_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_outcome_notice_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_outcome_notice_date', models.DateTimeField(null=True, blank=True)),
                ('potential_agreement_outcome_notice_alert_enabled', models.NullBooleanField()),
                ('potential_agreement_outcome_notice_alert_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_outcome_notice_alert_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_outcome_notice_alert_created', models.BooleanField()),
                ('potential_agreement_outcome_notice_alert_expired', models.BooleanField()),
                ('potential_agreement_outcome_notice_alert_date', models.DateTimeField(null=True, blank=True)),
                ('potential_agreement_expiration_alert_enabled', models.NullBooleanField()),
                ('potential_agreement_expiration_alert_time_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_expiration_alert_time_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_expiration_alert_created', models.BooleanField()),
                ('potential_agreement_expiration_alert_expired', models.BooleanField()),
                ('potential_agreement_expiration_alert_date', models.DateTimeField(null=True, blank=True)),
                ('potential_agreement_duration_details', models.TextField(null=True, blank=True)),
                ('potential_agreement_completed', models.BooleanField()),
                ('potential_agreement_system_created_date', models.DateTimeField()),
                ('potential_agreement_type', models.ForeignKey(related_name='potential_agreements', null=True, blank=True, to_field='agreement_type_id', to='agreement_type.AgreementType')),
                ('potential_agreement_user', models.ForeignKey(to='user.User', to_field='user_id', related_name='potential_agreements')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
