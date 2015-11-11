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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('asset_id', models.CharField(max_length=8, unique=True)),
                ('asset_path', models.CharField(max_length=2400)),
                ('asset_content_type', models.CharField(max_length=2400)),
                ('asset_original_name', models.CharField(max_length=2400)),
                ('asset_system_created_date', models.DateTimeField()),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
