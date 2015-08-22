# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('agreement_id', models.CharField(max_length=6, unique=True)),
                ('agreement_name', models.CharField(max_length=2400)),
                ('system_created_date', models.DateTimeField()),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
