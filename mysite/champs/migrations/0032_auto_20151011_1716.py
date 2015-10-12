# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0031_auto_20151011_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildcomponent',
            name='item_batch',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='buildcomponent',
            name='item_birth',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='buildcomponent',
            name='item_death',
            field=models.IntegerField(blank=True),
        ),
    ]
