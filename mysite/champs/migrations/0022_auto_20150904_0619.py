# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0021_auto_20150904_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
