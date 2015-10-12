# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('champ_name', models.CharField(max_length=200)),
                ('lane_name', models.CharField(max_length=200, choices=[(b'T', b'TOP'), (b'M', b'MIDDLE'), (b'B', b'BOTTOM'), (b'J', b'JUNGLE')])),
                ('role_name', models.CharField(max_length=200, choices=[(b'N', b'NONE'), (b'S', b'SOLO'), (b'D', b'DUO'), (b'DS', b'DUO_SUPPORT'), (b'DC', b'DUO_CARRY')])),
                ('league_name', models.CharField(max_length=200, choices=[(b'B', b'BRONZE'), (b'S', b'SILVER'), (b'G', b'GOLD'), (b'P', b'PLATINUM'), (b'D', b'DIAMOND'), (b'M', b'MASTER'), (b'C', b'CHALLENGER'), (b'U', b'UNRANKED')])),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
            ],
        ),
        migrations.CreateModel(
            name='Stats',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_id', models.CharField(max_length=200)),
                ('assists', models.IntegerField()),
                ('champ_level', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('double_kills', models.IntegerField()),
                ('first_blood_assist', models.IntegerField()),
                ('first_blood_kill', models.IntegerField()),
                ('first_inhibitor_assist', models.IntegerField()),
                ('first_inhibitor_kill', models.IntegerField()),
                ('first_tower_assist', models.IntegerField()),
                ('first_tower_kill', models.IntegerField()),
                ('gold_earned', models.IntegerField()),
                ('gold_spent', models.IntegerField()),
                ('inhibitor_kills', models.IntegerField()),
                ('item0', models.IntegerField()),
                ('item1', models.IntegerField()),
                ('item2', models.IntegerField()),
                ('item3', models.IntegerField()),
                ('item4', models.IntegerField()),
                ('item5', models.IntegerField()),
                ('item6', models.IntegerField()),
                ('killing_sprees', models.IntegerField()),
                ('kills', models.IntegerField()),
                ('largest_critical_strike', models.IntegerField()),
                ('largest_killing_spree', models.IntegerField()),
                ('largest_multi_kill', models.IntegerField()),
                ('magic_damage_dealt', models.IntegerField()),
                ('magic_damage_dealt_to_champions', models.IntegerField()),
                ('magic_damage_taken', models.IntegerField()),
                ('minions_killed', models.IntegerField()),
                ('neutral_minions_killed', models.IntegerField()),
                ('neutral_minions_killed_enemy_jungle', models.IntegerField()),
                ('neutral_minions_killed_team_jungle', models.IntegerField()),
                ('penta_kills', models.IntegerField()),
                ('physical_damage_dealt', models.IntegerField()),
                ('physical_damage_dealt_to_champions', models.IntegerField()),
                ('physical_damage_taken', models.IntegerField()),
                ('quadra_kills', models.IntegerField()),
                ('sight_wards_bought_in_game', models.IntegerField()),
                ('total_damage_dealt', models.IntegerField()),
                ('total_damage_dealt_to_champions', models.IntegerField()),
                ('total_damage_taken', models.IntegerField()),
                ('total_heal', models.IntegerField()),
                ('total_time_crowd_control_dealt', models.IntegerField()),
                ('total_units_healed', models.IntegerField()),
                ('tower_kills', models.IntegerField()),
                ('triple_kills', models.IntegerField()),
                ('true_damage_dealt', models.IntegerField()),
                ('true_damage_dealt_to_champions', models.IntegerField()),
                ('true_damage_taken', models.IntegerField()),
                ('unreal_kills', models.IntegerField()),
                ('vision_wards_bought_in_game', models.IntegerField()),
                ('wards_killed', models.IntegerField()),
                ('wards_placed', models.IntegerField()),
                ('winner', models.IntegerField()),
            ],
        ),
    ]
