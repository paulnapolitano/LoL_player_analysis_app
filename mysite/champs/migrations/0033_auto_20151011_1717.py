# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0032_auto_20151011_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buildcomponent',
            name='item_death',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
