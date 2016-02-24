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
            name='SmartView',
            fields=[
                ('primary_key', models.AutoField(serialize=False, primary_key=True)),
                ('id', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('query', jsonfield.fields.JSONField()),
                ('system_created_date', models.DateTimeField()),
                ('user', models.ForeignKey(to='user.User', to_field='id', related_name='smart_views')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
