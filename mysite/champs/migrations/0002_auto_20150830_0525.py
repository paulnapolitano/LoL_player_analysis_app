# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('game_id', models.CharField(max_length=200)),
                ('assists', models.IntegerField()),
                ('champ_level', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('double_kills', models.IntegerField()),
                ('first_blood_assist', models.BooleanField()),
                ('first_blood_kill', models.BooleanField()),
                ('first_inhibitor_assist', models.BooleanField()),
                ('first_inhibitor_kill', models.BooleanField()),
                ('first_tower_assist', models.BooleanField()),
                ('first_tower_kill', models.BooleanField()),
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
                ('winner', models.BooleanField()),
            ],
        ),
        migrations.DeleteModel(
            name='Stats',
        ),
        migrations.RemoveField(
            model_name='champ',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='statset',
            name='champ',
            field=models.ForeignKey(to='champs.Champ'),
        ),
    ]
