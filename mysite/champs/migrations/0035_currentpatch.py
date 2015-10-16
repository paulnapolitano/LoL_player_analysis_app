# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0034_auto_20151013_1349'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentPatch',
            fields=[
                ('patch', models.CharField(max_length=20, serialize=False, primary_key=True, blank=True)),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_datetime', models.DateTimeField(null=True, blank=True)),
                ('last_check', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
