# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0048_auto_20151026_2021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='championtag',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True),
        ),
    ]
