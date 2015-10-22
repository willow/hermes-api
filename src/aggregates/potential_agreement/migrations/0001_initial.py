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
            name='PotentialAgreement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('potential_agreement_id', models.CharField(max_length=8, unique=True)),
                ('potential_agreement_name', models.CharField(max_length=2400)),
                ('potential_agreement_artifacts', jsonfield.fields.JSONField(default=list)),
                ('potential_agreement_system_created_date', models.DateTimeField()),
                ('potential_agreement_user', models.ForeignKey(related_name='potential_agreements', to_field='user_id', to='user.User')),
            ],
            bases=(models.Model, src.libs.common_domain.aggregate_base.AggregateBase),
        ),
    ]
