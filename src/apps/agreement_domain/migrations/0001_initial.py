# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('potential_agreement_id', models.CharField(unique=True, max_length=8)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('system_created_date', models.DateTimeField()),
            ],
        ),
    ]
