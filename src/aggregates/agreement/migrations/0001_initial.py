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
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('agreement_uid', models.CharField(max_length=6, unique=True)),
                ('agreement_name', models.CharField(max_length=2400)),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
