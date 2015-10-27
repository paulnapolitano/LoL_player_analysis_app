# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0045_auto_20151020_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='gold_base',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='gold_purchasable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='gold_sell',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='item',
            name='gold_total',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
