# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import src.libs.common_domain.aggregate_base
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('user_id', models.CharField(unique=True, max_length=6)),
                ('user_name', models.CharField(max_length=2400)),
                ('user_nickname', models.CharField(max_length=2400)),
                ('user_email', models.EmailField(unique=True, max_length=254)),
                ('user_picture', models.URLField()),
                ('user_attrs', jsonfield.fields.JSONField()),
                ('system_created_date', models.DateTimeField()),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
