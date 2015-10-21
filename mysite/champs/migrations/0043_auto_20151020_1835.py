# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0042_auto_20151019_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_id',
            field=models.CharField(db_index=True, max_length=4, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='version',
            field=models.CharField(db_index=True, max_length=50, blank=True),
        ),
    ]
