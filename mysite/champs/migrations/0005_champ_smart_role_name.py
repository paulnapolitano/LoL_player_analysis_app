# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0004_auto_20150831_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='champ',
            name='smart_role_name',
            field=models.CharField(default='UNKNOWN', max_length=200),
            preserve_default=False,
        ),
    ]
