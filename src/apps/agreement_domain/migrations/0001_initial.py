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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('potential_agreement_id', models.CharField(max_length=6, unique=True)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('system_created_date', models.DateTimeField()),
                ('completed', models.BooleanField()),
            ],
        ),
    ]
