# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0041_item_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_id',
            field=models.CharField(max_length=4, blank=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
    ]
