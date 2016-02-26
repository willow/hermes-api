# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils import timezone
from src.aggregates.agreement_type.events import AgreementTypeCreated1
from src.libs.common_domain import event_store
from src.libs.python_utils.id.id_utils import generate_id


class Migration(migrations.Migration):
  dependencies = [
    ('common_domain', '0001_initial'),
  ]

  def create_defaults(apps, schema_editor):
    default_agreement_types = ['Consulting', 'Licensing', 'Sales']

    system_created_date = timezone.now()

    for at in default_agreement_types:
      id = generate_id()
      event = AgreementTypeCreated1(id, at, True, None, system_created_date)
      event_store.save_events(id, -1, [event])

  operations = [
    migrations.RunPython(create_defaults),
  ]
