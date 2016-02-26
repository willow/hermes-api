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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stream_id', models.CharField(max_length=255)),
                ('event_sequence', models.PositiveIntegerField()),
                ('event_name', models.CharField(max_length=1024)),
                ('event_data', jsonfield.fields.JSONField()),
                ('system_created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='event',
            unique_together=set([('stream_id', 'event_sequence')]),
        ),
    ]
