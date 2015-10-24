# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.libs.common_domain.aggregate_base
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('potential_agreement_id', models.CharField(unique=True, max_length=8)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('potential_agreement_artifacts', jsonfield.fields.JSONField(default=list)),
                ('potential_agreement_counterparty', models.CharField(max_length=2400, blank=True, null=True)),
                ('potential_agreement_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('potential_agreement_description', models.TextField(blank=True, null=True)),
                ('potential_agreement_execution_date', models.DateTimeField(blank=True, null=True)),
                ('potential_agreement_term_length_amount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('potential_agreement_term_length_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('potential_agreement_auto_renew', models.NullBooleanField()),
                ('potential_agreement_renewal_notice_amount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('potential_agreement_renewal_notice_type', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('potential_agreement_duration_details', models.TextField(blank=True, null=True)),
                ('potential_agreement_system_created_date', models.DateTimeField()),
                ('potential_agreement_user', models.ForeignKey(to='user.User', related_name='potential_agreements', to_field='user_id')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
