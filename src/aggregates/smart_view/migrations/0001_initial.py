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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('uid', models.CharField(unique=True, max_length=8)),
                ('name', models.CharField(max_length=2400)),
                ('query', jsonfield.fields.JSONField()),
                ('system_created_date', models.DateTimeField()),
                ('user', models.ForeignKey(related_name='smart_views', to='user.User', to_field='uid')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
