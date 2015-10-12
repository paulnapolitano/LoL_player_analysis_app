# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0019_auto_20150903_2103'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('summoner_id', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('rank', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='statset',
            name='matchVersion',
        ),
    ]
