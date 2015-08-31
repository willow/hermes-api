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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('potential_agreement_id', models.CharField(max_length=6, unique=True)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('system_created_date', models.DateTimeField()),
            ],
        ),
    ]
