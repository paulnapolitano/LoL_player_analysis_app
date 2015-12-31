# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0058_auto_20151115_2017'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchVersion',
            fields=[
                ('match_version', models.CharField(max_length=20, serialize=False, primary_key=True, blank=True)),
                ('dd_version', models.ForeignKey(to='champs.Version', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='champ',
            name='match_version',
            field=models.ForeignKey(blank=True, to='champs.MatchVersion', null=True),
        ),
    ]
