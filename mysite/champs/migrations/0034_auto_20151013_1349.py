# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0033_auto_20151011_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='img',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.CharField(max_length=4, serialize=False, primary_key=True),
        ),
    ]
