# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0037_auto_20151014_2227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='champ',
            name='champ_pk',
            field=models.CharField(max_length=30, serialize=False, primary_key=True, blank=True),
        ),
    ]
