# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0047_auto_20151026_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='championstatic',
            name='champ_id',
            field=models.CharField(db_index=True, max_length=4, blank=True),
        ),
        migrations.AddField(
            model_name='championtag',
            name='champion',
            field=models.ForeignKey(blank=True, to='champs.ChampionStatic', null=True),
        ),
        migrations.AddField(
            model_name='championtag',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=0, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='championstatic',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AlterField(
            model_name='championtag',
            name='tag',
            field=models.CharField(db_index=True, max_length=15, blank=True),
        ),
    ]
