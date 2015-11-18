# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0062_matchversion_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='region',
            field=models.CharField(db_index=True, max_length=3, null=True, blank=True),
        ),
    ]
