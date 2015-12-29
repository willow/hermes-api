# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('agreement_type', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('potential_agreement_id', models.CharField(max_length=8, unique=True)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('potential_agreement_artifacts', jsonfield.fields.JSONField(default=list)),
                ('potential_agreement_counterparty', models.CharField(max_length=2400, null=True, blank=True)),
                ('potential_agreement_description', models.TextField(null=True, blank=True)),
                ('potential_agreement_execution_date', models.DateTimeField(null=True, blank=True)),
                ('potential_agreement_term_length_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_term_length_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_auto_renew', models.NullBooleanField()),
                ('potential_agreement_renewal_notice_amount', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_renewal_notice_type', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('potential_agreement_duration_details', models.TextField(null=True, blank=True)),
                ('potential_agreement_system_created_date', models.DateTimeField()),
                ('potential_agreement_type', models.ForeignKey(to='agreement_type.AgreementType', blank=True, to_field='agreement_type_id', related_name='potential_agreements', null=True)),
                ('potential_agreement_user', models.ForeignKey(to_field='user_id', related_name='potential_agreements', to='user.User')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
