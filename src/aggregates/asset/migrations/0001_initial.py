# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('path', models.CharField(max_length=2400)),
                ('content_type', models.CharField(max_length=2400)),
                ('original_name', models.CharField(max_length=2400)),
                ('system_created_date', models.DateTimeField()),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
