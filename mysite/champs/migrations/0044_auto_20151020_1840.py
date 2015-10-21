# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0043_auto_20151020_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championstatic',
            name='id',
            field=models.CharField(max_length=4, serialize=False, primary_key=True, db_index=True),
        ),
    ]
