# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0040_remove_item_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='version',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
