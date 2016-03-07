# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('stream_id', models.CharField(max_length=255)),
                ('event_sequence', models.PositiveIntegerField()),
                ('event_type', models.CharField(max_length=1024)),
                ('event_name', models.CharField(max_length=1024)),
                ('event_data', jsonfield.fields.JSONField()),
                ('system_created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('stream_id', 'event_type', 'event_sequence')]),
        ),
    ]
