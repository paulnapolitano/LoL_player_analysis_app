# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0057_auto_20151115_2010'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Patch',
            new_name='Version',
        ),
        migrations.RenameField(
            model_name='version',
            old_name='patch',
            new_name='version',
        ),
        migrations.AlterField(
            model_name='championstatic',
            name='version',
            field=models.ForeignKey(to='champs.Version', blank=True, to_field='version'),
        ),
        migrations.AlterField(
            model_name='itemstatic',
            name='version',
            field=models.ForeignKey(to='champs.Version', blank=True, to_field='version'),
        ),
    ]
