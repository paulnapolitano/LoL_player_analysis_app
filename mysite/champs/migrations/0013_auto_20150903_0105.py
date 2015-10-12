# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0012_auto_20150903_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statset',
            name='champ',
        ),
        migrations.DeleteModel(
            name='Champ',
        ),
        migrations.DeleteModel(
            name='StatSet',
        ),
    ]
