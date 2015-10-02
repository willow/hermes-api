# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('potential_agreement_id', models.CharField(unique=True, max_length=8)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('potential_agreement_artifacts', jsonfield.fields.JSONField(default=list)),
                ('system_created_date', models.DateTimeField()),
            ],
        ),
    ]
