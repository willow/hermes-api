# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import src.libs.common_domain.aggregate_base


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmartView',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('smart_view_id', models.CharField(unique=True, max_length=8)),
                ('smart_view_name', models.CharField(max_length=2400)),
                ('smart_view_query', jsonfield.fields.JSONField()),
                ('smart_view_system_created_date', models.DateTimeField()),
                ('smart_view_user', models.ForeignKey(to='user.User', related_name='smart_views', to_field='user_id')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
