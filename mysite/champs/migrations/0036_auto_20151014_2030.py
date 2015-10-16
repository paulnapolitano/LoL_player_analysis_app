# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0035_currentpatch'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChampionStatic',
            fields=[
                ('id', models.CharField(max_length=4, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=20, blank=True)),
                ('img', models.CharField(max_length=50, blank=True)),
                ('stats_attack_range', models.FloatField(blank=True)),
                ('stats_mp_per_level', models.FloatField(blank=True)),
                ('stats_mp', models.FloatField(blank=True)),
                ('stats_ad', models.FloatField(blank=True)),
                ('stats_hp', models.FloatField(blank=True)),
                ('stats_hp_per_level', models.FloatField(blank=True)),
                ('stats_ad_per_level', models.FloatField(blank=True)),
                ('stats_armor', models.FloatField(blank=True)),
                ('stats_mp_regen_per_level', models.FloatField(blank=True)),
                ('stats_hp_regen', models.FloatField(blank=True)),
                ('stats_crit_per_level', models.FloatField(blank=True)),
                ('stats_spell_block_per_level', models.FloatField(blank=True)),
                ('stats_mp_regen', models.FloatField(blank=True)),
                ('stats_as_per_level', models.FloatField(blank=True)),
                ('stats_mr', models.FloatField(blank=True)),
                ('stats_ms', models.FloatField(blank=True)),
                ('stats_as_offset', models.FloatField(blank=True)),
                ('stats_crit', models.FloatField(blank=True)),
                ('stats_hp_regen_per_level', models.FloatField(blank=True)),
                ('stats_armor_per_level', models.FloatField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChampionTag',
            fields=[
                ('tag', models.CharField(max_length=15, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patch',
            fields=[
                ('patch', models.CharField(max_length=20, serialize=False, primary_key=True, blank=True)),
                ('region', models.CharField(max_length=20, blank=True)),
                ('start_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_datetime', models.DateTimeField(null=True, blank=True)),
                ('last_check', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='SpellStatic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('img', models.CharField(max_length=50, blank=True)),
                ('lv1_range', models.IntegerField(blank=True)),
                ('lv2_range', models.IntegerField(blank=True)),
                ('lv3_range', models.IntegerField(blank=True)),
                ('lv4_range', models.IntegerField(blank=True)),
                ('lv5_range', models.IntegerField(blank=True)),
                ('lv1_cd', models.IntegerField(blank=True)),
                ('lv2_cd', models.IntegerField(blank=True)),
                ('lv3_cd', models.IntegerField(blank=True)),
                ('lv4_cd', models.IntegerField(blank=True)),
                ('lv5_cd', models.IntegerField(blank=True)),
                ('lv1_cost', models.IntegerField(blank=True)),
                ('lv2_cost', models.IntegerField(blank=True)),
                ('lv3_cost', models.IntegerField(blank=True)),
                ('lv4_cost', models.IntegerField(blank=True)),
                ('lv5_cost', models.IntegerField(blank=True)),
                ('champion', models.ForeignKey(to='champs.ChampionStatic', blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='CurrentPatch',
        ),
    ]
