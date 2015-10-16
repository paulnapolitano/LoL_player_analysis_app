# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0038_auto_20151014_2246'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='championstatic',
            name='img',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_ad',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_ad_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_armor',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_armor_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_as_offset',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_as_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_attack_range',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_crit',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_crit_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_hp',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_hp_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_hp_regen',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_hp_regen_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_mp',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_mp_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_mp_regen',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_mp_regen_per_level',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_mr',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_ms',
        ),
        migrations.RemoveField(
            model_name='championstatic',
            name='stats_spell_block_per_level',
        ),
        migrations.AddField(
            model_name='championstatic',
            name='tags',
            field=models.ManyToManyField(to='champs.ChampionTag'),
        ),
    ]
