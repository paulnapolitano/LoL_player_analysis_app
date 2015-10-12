# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('champs', '0015_match_smartrolename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Champ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('champ_name', models.CharField(max_length=20)),
                ('champ_id', models.IntegerField()),
                ('smart_role_name', models.CharField(max_length=20)),
                ('role_name', models.CharField(max_length=20)),
                ('lane_name', models.CharField(max_length=20)),
                ('league_name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='StatSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('matchId', models.CharField(max_length=20)),
                ('summonerId', models.CharField(max_length=20)),
                ('matchVersion', models.CharField(max_length=20)),
                ('kills', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('deaths', models.IntegerField()),
                ('champLevel', models.IntegerField()),
                ('goldEarned', models.IntegerField()),
                ('goldSpent', models.IntegerField()),
                ('item0', models.IntegerField()),
                ('item1', models.IntegerField()),
                ('item2', models.IntegerField()),
                ('item3', models.IntegerField()),
                ('item4', models.IntegerField()),
                ('item5', models.IntegerField()),
                ('item6', models.IntegerField()),
                ('largestCriticalStrike', models.IntegerField()),
                ('killingSprees', models.IntegerField()),
                ('largestKillingSpree', models.IntegerField()),
                ('largestMultiKill', models.IntegerField()),
                ('magicDamageDealt', models.IntegerField()),
                ('magicDamageDealtToChampions', models.IntegerField()),
                ('magicDamageTaken', models.IntegerField()),
                ('minionsKilled', models.IntegerField()),
                ('neutralMinionsKilled', models.IntegerField()),
                ('neutralMinionsKilledEnemyJungle', models.IntegerField()),
                ('neutralMinionsKilledTeamJungle', models.IntegerField()),
                ('physicalDamageDealt', models.IntegerField()),
                ('physicalDamageDealtToChampions', models.IntegerField()),
                ('physicalDamageTaken', models.IntegerField()),
                ('sightWardsBoughtInGame', models.IntegerField()),
                ('totalDamageDealt', models.IntegerField()),
                ('totalDamageDealtToChampions', models.IntegerField()),
                ('totalDamageTaken', models.IntegerField()),
                ('totalHeal', models.IntegerField()),
                ('totalTimeCrowdControlDealt', models.IntegerField()),
                ('totalUnitsHealed', models.IntegerField()),
                ('doubleKills', models.IntegerField()),
                ('tripleKills', models.IntegerField()),
                ('quadraKills', models.IntegerField()),
                ('pentaKills', models.IntegerField()),
                ('unrealKills', models.IntegerField()),
                ('towerKills', models.IntegerField()),
                ('inhibitorKills', models.IntegerField()),
                ('firstBloodAssist', models.BooleanField()),
                ('firstBloodKill', models.BooleanField()),
                ('firstInhibitorAssist', models.BooleanField()),
                ('firstInhibitorKill', models.BooleanField()),
                ('firstTowerAssist', models.BooleanField()),
                ('firstTowerKill', models.BooleanField()),
                ('trueDamageDealt', models.IntegerField()),
                ('trueDamageDealtToChampions', models.IntegerField()),
                ('trueDamageTaken', models.IntegerField()),
                ('visionWardsBoughtInGame', models.IntegerField()),
                ('wardsPlaced', models.IntegerField()),
                ('wardsKilled', models.IntegerField()),
                ('winner', models.BooleanField()),
                ('champ', models.ForeignKey(to='champs.Champ')),
            ],
        ),
        migrations.DeleteModel(
            name='Match',
        ),
    ]
