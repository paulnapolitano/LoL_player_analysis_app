# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0056_auto_20151111_1657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championstatic',
            name='version',
            field=models.ForeignKey(to='champs.Patch', blank=True),
        ),
        migrations.AlterField(
            model_name='itemstatic',
            name='version',
            field=models.ForeignKey(to='champs.Patch', blank=True),
        ),
    ]
