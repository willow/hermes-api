# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('aggregate_id', models.CharField(max_length=255)),
                ('aggregate_name', models.CharField(max_length=255)),
                ('event_version', models.PositiveIntegerField()),
                ('event_name', models.CharField(max_length=1024)),
                ('event_data', jsonfield.fields.JSONField()),
            ],
        ),
    ]
