# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from src.aggregates.agreement_type.services import agreement_type_service
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):
  dependencies = [
    ('user', '0001_initial'),
    ('common_domain', '0001_initial'),

  ]

  def create_defaults(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    agreement_type_service.create_agreement_type('Consulting', True, None)
    agreement_type_service.create_agreement_type('Licensing', True, None)
    agreement_type_service.create_agreement_type('Sales', True, None)

  operations = [
    migrations.CreateModel(
      name='AgreementType',
      fields=[
        ('primary_key', models.AutoField(serialize=False, primary_key=True)),
        ('id', models.CharField(unique=True, max_length=8)),
        ('name', models.CharField(max_length=2400)),
        ('is_global', models.BooleanField()),
        ('system_created_date', models.DateTimeField()),
        ('user',
         models.ForeignKey(related_name='user_agreement_types', null=True, to_field='id', to='user.User', blank=True)),
      ],
      bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
    ),
    migrations.AlterUniqueTogether(
      name='agreementtype',
      unique_together=set([('name', 'user')]),
    ),
    migrations.RunPython(create_defaults),
  ]
