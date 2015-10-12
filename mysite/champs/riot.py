# Contains aggregated stat info
class AggregatedStatsDto:
    def __init__(self, dict):
        if 'averageAssists' in dict:
            self.avg_assists = dict['averageAssists']
        if 'averageChampionsKilled' in dict:
            self.avg_kills = dict['averageChampionsKilled']
        if 'averageCombatPlayerScore' in dict: 
            self.avg_combat_score = dict['averageCombatPlayerScore']
        self.avg_node_cap = dict['averageNodeCapture']  #D
        self.avg_node_cap_assist = dict['averageNodeCaptureAssist'] #D
        self.avg_node_neut = dict['averageNodeNeutralize'] #D
        self.avg_node_neut_assist = dict['averageNodeNeutralizeAssist'] #D
        self.avg_deaths = dict['averageNumDeaths'] #D
        self.avg_obj_score = dict['averageObjectivePlayerScore'] #D
        self.avg_team_obj = dict['averageTeamObjective'] #D
        self.avg_total_score = dict['averageTotalPlayerScore'] #D
        self.num_bot_games = dict['botGamesPlayed']
        self.killing_spree = dict['killingSpree'] 
        self.max_assists = dict['maxAssists'] #D
        self.max_kills = dict['maxChampionsKilled']
        self.max_combat_score = dict['maxCombatPlayerScore'] #D
        self.max_largest_crit = dict['maxLargestCriticalStrike']
        self.max_largest_spree = dict['maxLargestKillingSpree']
        self.max_node_cap = dict['maxNodeCapture'] #D
        self.max_node_cap_assist = dict['maxNodeCaptureAssist'] #D
        self.max_node_neut = dict['maxNodeNeutralize'] #D
        self.max_node_neut_assist = dict['maxNodeNeutralizeAssist'] #D
        self.max_num_deaths = dict['maxNumDeaths'] #D
        self.max_obj_score = dict['maxObjectivePlayerScore'] #D
        self.max_team_obj = dict['maxTeamObjective'] #D
        self.max_time_played = dict['maxTimePlayed']
        self.max_time_spent_living = dict['maxTimeSpentLiving']
        self.max_total_score = dict['maxTotalPlayerScore'] #D
        self.most_kills_per_session = dict['mostChampionKillsPerSession']
        self.most_spells_cast = dict['mostSpellsCast']
        self.normal_games_played = dict['normalGamesPlayed']
        self.ranked_premade_games_played = dict['rankedPremadeGamesPlayed']
        self.ranked_solo_games_played = dict['rankedSoloGamesPlayed']
        self.total_assists = dict['totalAssists']
        self.total_champion_kills = dict['totalChampionKills']
        self.total_damage_dealt = dict['totalDamageDealt']
        self.total_damage_taken = dict['totalDamageTaken']
        self.total_deaths_per_session = dict['totalDeathsPerSession'] #Ranked only
        self.total_double_kills = dict['totalDoubleKills']
        self.total_first_blood = dict['totalFirstBlood']
        self.total_gold_earned = dict['totalGoldEarned']
        self.total_heal = dict['totalHeal']
        self.total_magic_damage_dealt = dict['totalMagicDamageDealt']
        self.total_minion_kills = dict['totalMinionKills']
        self.total_neutral_minions_killed = dict['totalNeutralMinionsKilled']
        self.total_node_capture = dict['totalNodeCapture'] #D
        self.total_node_neutralize = dict['totalNodeNeutralize'] #D
        self.total_penta_kills = dict['totalPentaKills']
        self.total_physical_damage_dealt = dict['totalPhysicalDamageDealt']
        self.total_quadra_kills = dict['totalQuadraKills']
        self.total_sessions_lost = dict['totalSessionsLost']
        self.total_sessions_played = dict['totalSessionsPlayed']
        self.total_sessions_won = dict['totalSessionsWon']
        self.total_triple_kills = dict['totalTripleKills']
        self.total_turrets_killed = dict['totalTurretsKilled']
        self.total_unreal_kills = dict['totalUnrealKills']

class BannedChampion:
    def __init__(self, dict):
        self.champion_id = dict['championId']
        self.pick_turn = dict['pickTurn']
        if 'teamId' in dict:
            self.team_id = dict['teamId']

class BasicDataDto:
    def __init__(self, dict):
        self.colloq = dict['colloq']
        self.consume_on_full = dict['consumeOnFull']
        self.consumed = dict['consumed']
        self.depth = dict['depth']
        self.description = dict['description']
        self.frum = dict['from']
        self.gold = GoldDto(dict['gold'])
        self.group = dict['group']
        self.hide_from_all = dict['hideFromAll']
        self.id = dict['id']
        self.image = ImageDto(dict['image'])
        self.in_store = dict['inStore']
        self.into = dict['into']
        self.maps = dict['maps']
        self.name = dict['name'] 
        self.plaintext = dict['plaintext']
        self.required_champion = dict['requiredChampion']
        self.rune = MetaDataDto(dict['rune'])
        self.sanitized_description = dict['sanitizedDescription']
        self.special_recipe = dict['specialRecipe']
        self.stacks = dict['stacks']
        self.stats = BasicDataStatsDto(dict['stats'])
        self.tags = dict['tags']
        
class BasicDataStatsDto:
    def __init__(self, dict):
        self.flat_armor_mod = dict['FlatArmorMod']
        self.flat_attack_speed_mod = dict['FlatAttackSpeedMod']
        self.flat_armor_mod = dict['FlatArmorMod']		
        self.flat_attack_speed_mod = dict['FlatAttackSpeedMod']		
        self.flat_block_mod = dict['FlatBlockMod']		
        self.flat_crit_chance_mod = dict['FlatCritChanceMod']
        self.flat_crit_damage_mod = dict['FlatCritDamageMod']
        self.flat_expbonus = dict['FlatEXPBonus']
        self.flat_energy_pool_mod = dict['FlatEnergyPoolMod']
        self.flat_energy_regen_mod = dict['FlatEnergyRegenMod']
        self.flat_hppool_mod = dict['FlatHPPoolMod']
        self.flat_hpregen_mod = dict['FlatHPRegenMod']
        self.flat_mppool_mod = dict['FlatMPPoolMod']
        self.flat_mpregen_mod = dict['FlatMPRegenMod']
        self.flat_magic_damage_mod = dict['FlatMagicDamageMod']
        self.flat_movement_speed_mod = dict['FlatMovementSpeedMod']
        self.flat_physical_damage_mod = dict['FlatPhysicalDamageMod']
        self.flat_spell_block_mod = dict['FlatSpellBlockMod']
        self.percent_armor_mod = dict['PercentArmorMod']
        self.percent_attack_speed_mod = dict['PercentAttackSpeedMod']
        self.percent_block_mod = dict['PercentBlockMod']
        self.percent_crit_chance_mod = dict['PercentCritChanceMod']
        self.percent_crit_damage_mod = dict['PercentCritDamageMod']
        self.percent_dodge_mod = dict['PercentDodgeMod']
        self.percent_expbonus = dict['PercentEXPBonus']
        self.percent_hppool_mod = dict['PercentHPPoolMod']
        self.percent_hpregen_mod = dict['PercentHPRegenMod']
        self.percent_life_steal_mod = dict['PercentLifeStealMod']
        self.percent_mppool_mod = dict['PercentMPPoolMod']
        self.percent_mpregen_mod = dict['PercentMPRegenMod']
        self.percent_magic_damage_mod = dict['PercentMagicDamageMod']
        self.percent_movement_speed_mod = dict['PercentMovementSpeedMod']
        self.percent_physical_damage_mod = dict['PercentPhysicalDamageMod']
        self.percent_spell_block_mod = dict['PercentSpellBlockMod']
        self.percent_spell_vamp_mod = dict['PercentSpellVampMod']
        self.r_flat_armor_mod_per_level = dict['rFlatArmorModPerLevel']
        self.r_flat_armor_penetration_mod = dict['rFlatArmorPenetrationMod']
        self.r_flat_armor_penetration_mod_per_level = dict['rFlatArmorPenetrationModPerLevel']
        self.r_flat_crit_chance_mod_per_level = dict['rFlatCritChanceModPerLevel']
        self.r_flat_crit_damage_mod_per_level = dict['rFlatCritDamageModPerLevel']
        self.r_flat_dodge_mod = dict['rFlatDodgeMod']
        self.r_flat_dodge_mod_per_level = dict['rFlatDodgeModPerLevel']
        self.r_flat_energy_mod_per_level = dict['rFlatEnergyModPerLevel']
        self.r_flat_energy_regen_mod_per_level = dict['rFlatEnergyRegenModPerLevel']
        self.r_flat_gold_per_mod = dict['rFlatGoldPer10Mod']
        self.r_flat_hpmod_per_level = dict['rFlatHPModPerLevel']
        self.r_flat_hpregen_mod_per_level = dict['rFlatHPRegenModPerLevel']
        self.r_flat_mpmod_per_level = dict['rFlatMPModPerLevel']
        self.r_flat_mpregen_mod_per_level = dict['rFlatMPRegenModPerLevel']
        self.r_flat_magic_damage_mod_per_level = dict['rFlatMagicDamageModPerLevel']
        self.r_flat_magic_penetration_mod = dict['rFlatMagicPenetrationMod']
        self.r_flat_magic_penetration_mod_per_level = dict['rFlatMagicPenetrationModPerLevel']
        self.r_flat_movement_speed_mod_per_level = dict['rFlatMovementSpeedModPerLevel']
        self.r_flat_physical_damage_mod_per_level = dict['rFlatPhysicalDamageModPerLevel']
        self.r_flat_spell_block_mod_per_level = dict['rFlatSpellBlockModPerLevel']
        self.r_flat_time_dead_mod = dict['rFlatTimeDeadMod']
        self.r_flat_time_dead_mod_per_level = dict['rFlatTimeDeadModPerLevel']
        self.r_percent_armor_penetration_mod = dict['rPercentArmorPenetrationMod']
        self.r_percent_armor_penetration_mod_per_level = dict['rPercentArmorPenetrationModPerLevel']
        self.r_percent_attack_speed_mod_per_level = dict['rPercentAttackSpeedModPerLevel']
        self.r_percent_cooldown_mod = dict['rPercentCooldownMod']
        self.r_percent_cooldown_mod_per_level = dict['rPercentCooldownModPerLevel']
        self.r_percent_magic_penetration_mod = dict['rPercentMagicPenetrationMod']
        self.r_percent_magic_penetration_mod_per_level = dict['rPercentMagicPenetrationModPerLevel']
        self.r_percent_movement_speed_mod_per_level = dict['rPercentMovementSpeedModPerLevel']
        self.r_percent_time_dead_mod = dict['rPercentTimeDeadMod']
        self.r_percent_time_dead_mod_per_level = dict['rPercentTimeDeadModPerLevel']
        
class BlockDto:
    def __init__(self, dict):
        self.items = [BlockItemDto(item) for item in dict['items']]
        self.rec_math = dict['recMath']
        self.type = dict['type']
        
class BlockItemDto:
    def __init__(self, dict):
        self.count = dict['count']
        self.id = dict['id']

# This object contains champion information.        
class ChampionDto:
    def __init__(self, dict):
        if 'allytips' in dict:
            self.ally_tips = dict['allytips']
        if 'blurb' in dict:
            self.blurb = dict['blurb']
        if 'enemytips' in dict:
            self.enemytips = dict['enemytips']
        if 'image' in dict:
            self.image = dict['image']
        if 'info' in dict: 
            self.info = dict['info']
        if 'lore' in dict:
            self.lore = dict['lore']
        if 'partype' in dict:
            self.partype = dict['partype']
        if 'passive' in dict:
            self.passive = PassiveDto(dict['passive'])
        if 'recommended' in dict:
            self.recommended = [RecommendedDto(el) for el in dict['recommended']]
        if 'skins' in dict:
            self.skins = [SkinDto(skin) for skin in dict['skins']]
        if 'spells' in dict:
            self.spells = [ChampionSpellDto(spell) for spell in dict['spells']]
        if 'stats' in dict:
            self.stats = StatsDto(dict['stats'])
        if 'tags' in dict:
            self.tags = dict['tags']
            
        self.id = dict['id']
        self.key = dict['key']
        self.name = dict['name']            
        self.title = dict['title']
        
    def __str__(self):
        string = ''
        for key in self.__dict__:
            string += '{key}: {val}\n'.format(
                key=key,
                val=self.__dict__[key]
            )
        return string        

# This object contains a collection of champion information.     
class ChampionListDto:
    def __init__(self, dict):
        if 'format' in dict:
            self.format = dict['format']
        if 'keys' in dict:
            self.keys = dict['keys']
        
        self.data = {}
        for key in dict['data']:
            self.data[key] = ChampionDto(dict['data'][key]) 
        self.type = dict['type']
        self.version = dict['version']
        
    def __str__(self):
        string = ''
        for key in self.data:
            string += '{champ_dto}\n'.format(champ_dto=str(self.data[key]))
        return string
        
class ChampionInfoDto:
    def __init__(self, dict):
        self.active = dict['active']
        self.bot_enabled = dict['botEnabled']
        self.bot_mm_enabled = dict['botMmEnabled']
        self.free_to_play = dict['freeToPlay']
        self.id = dict['id']
        self.ranked_play_enabled = dict['rankedPlayEnabled']
    def __str__(self):
        string = 'Active: {}\n'.format(self.active)
        string += 'Bot Enabled: {}\n'.format(self.bot_enabled)
        string += 'Bot Match Made Enabled: {}\n'.format(self.bot_mm_enabled)
        string += 'Free to Play: {}\n'.format(self.free_to_play)
        string += 'ID: {}\n'.format(self.id)
        string += 'Ranked Play Enabled: {}\n'.format(self.ranked_play_enabled)
        return string
    def get_active(self):
        return self.active
    def get_bot_enabled(self):
        return self.bot_enabled
    def get_bot_mm_enabled(self):
        return self.bot_mm_enabled
    def get_free_to_play(self):
        return self.free_to_play
    def get_id(self):
        return self.id
    def get_ranked_play_enabled(self):
        return self.ranked_play_enabled
        
class ChampionInfoListDto:
    def __init__(self, dict):
        self.champ_list = [ChampionInfoDto(ch) for ch in dict['champions']]
    def get_champ(self, id):
        for champ in self.champ_list:
            if champ.get_id() == id:
                return champ
        return None
    def __str__(self):
        string = ''
        for champ in self.champ_list:
            string += str(champ) + '\n'
        return string

class ChampionSpellDto:
    def __init__(self, dict):
        self.alt_images = [ImageDto(image) for image in dict['altimages']]
        self.cooldown = dict['cooldown']
        self.cooldown_burn = dict['cooldownBurn']
        self.cost = dict['cost']
        self.cost_burn = dict['costBurn']
        self.cost_type = dict['costType']
        self.description = dict['description']
        self.effect = dict['effect']
        self.effect_burn = dict['effectBurn']
        self.image = ImageDto(dict['image'])
        self.key = dict['key']
        self.level_tip = LevelTipDto(dict['leveltip'])
        self.max_rank = dict['maxrank']
        self.name = dict['name']
        self.range = dict['range']
        self.range_burn = dict['rangeBurn']
        self.resource = dict['resource']
        self.sanitized_description = dict['sanitizedDescription']
        self.sanitized_tooltip = dict['sanitizedTooltip']
        self.tooltip = dict['tooltip']
        self.vars = [SpellVarsDto(var) for var in dict['vars']]
  
# Contains champion id and aggregated stats associated with that champ  
class ChampionStatsDto:
	def __init__(self, dict):
		self.id = dict['id']
		self.stats = AggregatedStatsDto(dict['stats'])
        
class CurrentGameInfo:
    def __init__(self, dict):
        self.banned_champions = [BannedChampion(champ) 
                                 for champ in dict['bannedChampions']]
        self.game_id = dict['gameId']
        self.game_length = dict['gameLength']
        self.game_mode = dict['gameMode']
        self.game_queue_config_id = dict['gameQueueConfigId']
        self.game_start_time = dict['gameStartTime']
        self.game_type = dict['gameType']
        self.map_id = dict['mapId'] 
        self.observers = Observer(dict['observers'])
        self.participants = [CurrentGameParticipant(participant) 
                             for participant in dict['participants']]
        self.platform_id = dict['platformId']

class CurrentGameParticipant:
    def __init__(self, dict):
        self.bot = dict['bot']
        self.champion_id = dict['championId']
        self.masteries = [Mastery(mast_d) for mast_d in dict['masteries']]
        self.profile_icon_id = dict['profileIconId']
        self.runes = [Rune(rune_dict) for rune_dict in dict['runes']]
        self.spell1_id = dict['spell1Id']
        self.spell2_id = dict['spell2Id']
        self.summoner_id = dict['summonerId']
        self.summoner_name = dict['summonerName']
        self.team_id = dict['teamId']
 
class Event:
    def __init__(self, dict):
        if 'ascendedType' in dict:
            self.ascended_type = dict['ascendedType']
        if 'assistingParticipantIds' in dict:
            self.assisting_participant_ids = dict['assistingParticipantIds']
        if 'buildingType' in dict:
            self.building_type = dict['buildingType']
        if 'creatorId' in dict:
            self.creator_id = dict['creatorId']
        if 'eventType' in dict:
            self.event_type = dict['eventType']
        if 'itemAfter' in dict:
            self.item_after = dict['itemAfter']
        if 'itemBefore' in dict:
            self.item_before = dict['itemBefore']
        if 'itemId' in dict:
            self.item_id = dict['itemId']
        if 'killerId' in dict:
            self.killer_id = dict['killerId']
        if 'laneType' in dict:
            self.lane_type = dict['laneType']
        if 'levelUpType' in dict:
            self.level_up_type = dict['levelUpType']
        if 'monsterType' in dict:
            self.monster_type = dict['monsterType']
        if 'participantId' in dict:
            self.participant_id = dict['participantId']
        if 'pointCaptured' in dict:
            self.point_captured = dict['pointCaptured']
        if 'position' in dict:
            self.position = Position(dict['position'])
        if 'skillSlot' in dict:
            self.skill_slot = dict['skillSlot']
        if 'teamId' in dict:
            self.team_id = dict['teamId']
        if 'timestamp' in dict:
            self.timestamp = dict['timestamp']
        if 'towerType' in dict:
            self.tower_type = dict['towerType']
        if 'victimId' in dict:
            self.victim_id = dict['victimId']
        if 'wardType' in dict:
            self.ward_type = dict['wardType'] 
 
class FeaturedGameInfo:
    def __init__(self, dict):
        self.banned_champions = [BannedChampion(champ) 
                                 for champ in dict['bannedChampions']]
        self.game_id = dict['gameId']
        self.game_length = dict['gameLength']
        self.game_mode = dict['gameMode']
        self.game_queue_config_id = dict['gameQueueConfigId']
        self.game_start_time = dict['gameStartTime']
        self.game_type = dict['gameType']
        self.map_id = dict['mapId'] 
        self.observers = Observer(dict['observers'])
        self.participants = [CurrentGameParticipant(participant) 
                             for participant in dict['participants']]
        self.platform_id = dict['platformId']
        
class FeaturedGames:
    def __init__(self, dict):
        self.client_refresh_interval = dict['clientRefreshInterval']
        self.game_list = [FeaturedGameInfo(game) for game in dict['gameList']]

class Frame:
    def __init__(self, dict):
        if 'events' in dict:
            self.events = [Event(el) for el in dict['events']]
        self.participant_frames = {}
        for key in dict['participantFrames']:
            self.participant_frames[key] = ParticipantFrame(dict['participantFrames'][key])
        self.timestamp = dict['timestamp']
       
class GameDto:
    def __init__(self, dict):
        self.champion_id = dict['championId']
        self.create_date = dict['createDate']
        self.fellow_players = [PlayerDto(player) 
                               for player in dict['fellowPlayers']]
        self.game_id = dict['gameId']
        self.game_mode = dict['gameMode']
        self.game_type = dict['gameType']
        self.invalid = dict['invalid']
        self.ip_earned = dict['ipEarned']
        self.level = dict['level']
        self.map_id = dict['mapId']
        self.spell1 = dict['spell1']
        self.spell2 = dict['spell2']
        self.stats = RawStatsDto(dict['stats'])
        
        global SUB_TYPES
        if dict['subType'] in SUB_TYPES:
            self.sub_type = dict['subType']
        else:
            self.sub_type = 'NOT_RECOGNIZED'

class GoldDto:
    def __init__(self, dict):
        self.base = dict['base']
        self.purchasable = dict['purchasable']
        self.sell = dict['sell']
        self.total = dict['total']
          
class GroupDto:
    def __init__(self, dict):
        self.max_group_ownable = dict['MaxGroupOwnable']
        self.key = dict['key']
            
class ImageDto:
    def __init__(self, dict):
        self.full = dict['full']
        self.group = dict['group']
        self.h = dict['h']
        self.sprite = dict['sprite']
        self.w = dict['w']
        self.x = dict['x']
        self.y = dict['y']
   
class Incident:
    def __init__(self, dict):
        self.active = dict['active']
        self.created_at = dict['created_at']
        self.id = dict['id']
        self.updates = [Message(el) for el in dict['updates']]
   
class InfoDto:
    def __init__(self, dict):
        self.attack = dict['attack']
        self.defense = dict['defense']
        self.difficulty = dict['difficulty']
        self.magic = dict['magic']

class ItemDto:
    def __init__(self, dict):
        self.colloq = dict['colloq']
        self.consume_on_full = dict['consumeOnFull']
        self.consumed = dict['consumed']
        self.depth = dict['depth']
        self.description = dict['description']
        self.frum = dict['from']
        self.gold = GoldDto(dict['gold'])
        self.group = dict['group']
        self.hide_from_all = dict['hideFromAll']
        self.id = dict['id']
        self.image = ImageDto(dict['image'])
        self.in_store = dict['inStore']
        self.into = dict['into']
        self.maps = dict['maps']
        self.name = dict['name'] 
        self.plaintext = dict['plaintext']
        self.required_champion = dict['requiredChampion']
        self.rune = MetaDataDto(dict['rune'])
        self.sanitized_description = dict['sanitizedDescription']
        self.special_recipe = dict['specialRecipe']
        self.stacks = dict['stacks']
        self.stats = BasicDataStatsDto(dict['stats'])
        self.tags = dict['tags']
        
class ItemListDto:
    def __init__(self, dict):
        self.basic = BasicDataDto(dict['basic'])
        self.data = {}
        for key in dict['data']:
            self.data[key] = ItemDto(dict['data'][key])
        self.groups = [GroupDto(grp) for grp in dict['groups']] 
        self.tree = [ItemTreeDto(item) for item in dict['tree']]
        self.type = dict['type']
        self.version = dict['version']
 
class ItemTreeDto:
    def __init__(self, dict):
        self.header = dict['header']
        self.tags = dict['tags']
 
class LanguageStringsDto:
    def __init__(self, dict):
        self.data = dict['data']
        self.type = dict['type']
        self.version = dict['version']
 
class LeagueDto:
    def __init__(self, dict):
        self.entries = [LeagueEntryDto(entry) for entry in dict['entries']]
        self.name = dict['name']
        self.participant_id = dict['participantId']
        self.queue = dict['queue']
        self.tier = dict['tier']
        
class LeagueEntryDto:
    def __init__(self, dict):
        self.division = dict['division']
        self.is_fresh_blood = dict['isFreshBlood']
        self.is_hot_streak = dict['isHotStreak']
        self.is_inactive = dict['isInactive']
        self.is_veteran = dict['isVeteran']
        self.league_points = dict['leaguePoints']
        self.losses = dict['losses']
        self.mini_series = MiniSeriesDto(dict['miniSeries'])
        self.player_or_team_id = dict['playerOrTeamId']
        self.player_or_team_name = dict['playerOrTeamName']
        self.wins = dict['wins']

class LevelTipDto:
    def __init__(self, dict):
        self.effect = dict['effect']
        self.label = dict['label']
     
class MapDataDto:
    def __init__(self, dict):
        self.data = {}
        for key in dict['data']:
            self.data[key] = MapDetailsDto(dict['data'][key])
        self.type = dict['type']
        self.version = dict['version']
     
class MapDetailsDto:
    def __init__(self, dict):
        self.image = ImageDto(dict['image'])
        self.map_id = dict['mapId']
        self.map_name = dict['mapName']
        self.unpurchasable_item_list_list = dict['unpurchasableItemList']

class Mastery:
    def __init__(self, dict):
        self.mastery_id = dict['masteryId']
        self.rank = dict['rank']

class MasteryDto:
    def __init__(self, dict):
		self.description = dict['description']
		self.id = dict['id']
		self.image = ImageDto(dict['image'])
		self.mastery_tree = dict['masteryTree']
		self.name = dict['name']
		self.prereq = dict['prereq']
		self.ranks = dict['ranks']
		self.sanitized_description = dict['sanitizedDescription']    

class MasteryDtoSimple:
    def __init__(self, dict):
		self.id = dict['id']
		self.rank = dict['rank'] 
        
class MasteryListDto:
    def __init__(self, dict):
        self.data = {}
        for key in dict['data']:
            self.data[key] = MasteryDto(dict['data'][key])
        self.tree = MasteryTreeDto(dict['tree'])
        self.type = dict['type']
        self.version = dict['version']
 
class MasteryPageDto:
	def __init__(self, dict):
		self.current = dict['current']
		self.id = dict['id']
		self.masteries = [MasteryDtoSimple(el) for el in dict['masteries']]
		self.name = dict['name'] 
 
class MasteryPagesDto:
	def __init__(self, dict):
		self.pages = Set[MasteryPageDto](dict['pages'])
		self.summoner_id = dict['summonerId'] 
 
class MasteryTreeDto:
    def __init__(self, dict):
        self.defense = [MasteryTreeListDto(el) for el in dict['Defense']]
        self.offense = [MasteryTreeListDto(el) for el in dict['Offense']]
        self.utility = [MasteryTreeListDto(el) for el in dict['Utility']]      

class MasteryTreeItemDto:
    def __init__(self, dict):
        self.mastery_id = dict['masteryId']
        self.prereq = dict['prereq']
        
class MasteryTreeListDto:
    def __init__(self, dict):
        self.mastery_tree_items = [MasteryTreeItemDto(el) for el in dict['masteryTreeItems']]

class MatchDetail:
    def __init__(self, dict):
        self.map_id = dict['mapId']
        self.match_creation = dict['matchCreation']
        self.match_duration = dict['matchDuration']
        self.match_id = dict['matchId']
        self.match_mode = dict['matchMode']
        self.match_type = dict['matchType']
        self.match_version = dict['matchVersion']
        self.participant_identities = [ParticipantIdentity(el) for el in dict['participantIdentities']]
        self.participants = [Participant(el) for el in dict['participants']]
        self.platform_id = dict['platformId']
        self.queue_type = dict['queueType']
        self.region = dict['region']
        self.season = dict['season']
        self.teams = [Team(el) for el in dict['teams']]
        self.timeline = Timeline(dict['timeline'])
        
    def get_map_id(self):
        return self.map_id
    def get_match_creation(self):
        return self.match_creation
    def get_match_duration(self):
        return self.match_duration
    def get_match_id(self):
        return self.match_id
    def get_match_mode(self):
        return self.match_mode
    def get_match_type(self):
        return self.match_type
    def get_match_version(self):
        return self.match_version
    def get_participant_identities(self):
        return self.participant_identities
    def get_participants(self):
        return self.participants
    def get_platform_id(self):
        return self.platform_id
    def get_queue_type(self):
        return self.queue_type
    def get_region(self):
        return self.region
    def get_season(self):
        return self.season
    def get_teams(self):
        return self.teams
    def get_timeline(self):
        return self.timeline
    
class MatchHistorySummaryDto:
	def __init__(self, dict):
		self.assists = dict['assists']
		self.date = dict['date']
		self.deaths = dict['deaths']
		self.game_id = dict['gameId']
		self.game_mode = dict['gameMode']
		self.invalid = dict['invalid']
		self.kills = dict['kills']
		self.map_id = dict['mapId']
		self.opposing_team_kills = dict['opposingTeamKills']
		self.opposing_team_name = dict['opposingTeamName']
		self.win = dict['win']
    
class MatchList:
	def __init__(self, dict):
		self.end_index = dict['endIndex']
		self.matches = [MatchReference(el) for el in dict['matches']]
		self.start_index = dict['startIndex']
		self.total_games = dict['totalGames']
     
class MatchReference: 
	def __init__(self, dict):
		self.champion = dict['champion']
		self.lane = dict['lane']
		self.match_id = dict['matchId']
		self.platform_id = dict['platformId']
		self.queue = dict['queue']
		self.role = dict['role']
		self.season = dict['season']
		self.timestamp = dict['timestamp']
        
class MatchSummary:
    def __init__(self, dict):
		self.map_id = dict['mapId']
		self.match_creation = dict['matchCreation']
		self.match_duration = dict['matchDuration']
		self.match_id = dict['matchId']
		self.match_mode = dict['matchMode']
		self.match_type = dict['matchType']
		self.match_version = dict['matchVersion']
		self.participant_identities = [ParticipantIdentity(el) for el in dict['participantIdentities']]
		self.participants = [Participant(el) for el in dict['participants']]
		self.platform_id = dict['platformId']
		self.queue_type = dict['queueType']
		self.region = dict['region']
		self.season = dict['season']
        
    def __str__(self):
        string = ''
        my_dict = self.__dict__
        my_dict_sorted = sorted(my_dict)
        for key in my_dict_sorted:
            if key == 'participant_identities':
                string += '\tparticipant_identities:\n'
                i = 0
                for participant in my_dict['participant_identities']:
                    string += '\t\tParticipant #{}: \n{}'.format(i, participant)
                    i += 1
            elif key == 'participants':
                string += '\tparticipants:\n'
                i = 0
                for participant in my_dict['participants']:
                    string += '\t\tParticipant #{}: \n{}'.format(i, participant)
                    i += 1
            else:
                string += '\t{}: {}\n'.format(key, self.__dict__[key])
        return string
        
class Message:
    def __init__(self, dict):
		self.author = dict['author']
		self.content = dict['content']
		self.created = dict['created_at']
		self.id = dict['id']
		self.severity = dict['severity']
		self.translations = [Translation(el) for el in dict['translations']]
		self.updated = dict['updated_at']     
       
class MetaDataDto:
    def __init__(self, dict):
		self.is_rune = dict['isRune']
		self.tier = dict['tier']
		self.type = dict['type']        
        
class MiniSeriesDto:
    def __init__(self, dict):
        self.losses = dict['losses']
        self.progress = dict['progress']
        self.target = dict['target']
        self.wins = dict['wins']
        
class Observer:
    def __init__(self, key):
        self.encryption_key = key

class Participant:
    def __init__(self, dict):
		self.champion_id = dict['championId']
		self.highest_achieved_season_tier = dict['highestAchievedSeasonTier']
		self.masteries = [Mastery(el) for el in dict['masteries']]
		self.participant_id = dict['participantId']
		self.runes = [Rune(el) for el in dict['runes']]
		self.spell1_id = dict['spell1Id']
		self.spell2_id = dict['spell2Id']
		self.stats = ParticipantStatsSR(dict['stats'])
		self.team_id = dict['teamId']
		self.timeline = ParticipantTimeline(dict['timeline'])   
        
    def __str__(self):
        string = ''
        for key in self.__dict__:
            string += '\t\t{}: {}\n'.format(key, self.__dict__[key])
        return string
        
    def get_champion_id(self):
        return self.champion_id
    def get_highest_achieved_season_tier(self):
        return self.highest_achieved_season_tier
    def get_masteries(self):
        return self.masteries
    def get_participant_id(self):
        return self.participant_id
    def get_runes(self):
        return self.runes
    def get_spell1_id(self):
        return self.spell1_id
    def get_spell2_id(self):
        return self.spell2_id
    def get_stats(self):
        return self.stats
    def get_team_id(self):
        return self.team_id
    def get_timeline(self):
        return self.timeline
        
class ParticipantFrame:
    def __init__(self, dict):
        self.current_gold = dict['currentGold']
        self.dominion_score = dict['dominionScore']
        self.jungle_minions_killed = dict['jungleMinionsKilled']
        self.level = dict['level']
        self.minions_killed = dict['minionsKilled']
        self.participant_id = dict['participantId']
        if 'position' in dict: 
            self.position = Position(dict['position'])
        self.team_score = dict['teamScore']
        self.total_gold = dict['totalGold']
        self.xp = dict['xp']
        
class ParticipantIdentity:
    def __init__(self, dict):
        if 'participantId' in dict:
            self.participant_id = dict['participantId']
        if 'player' in dict:
            self.player = Player(dict['player'])
        
    def __str__(self):
        string = ''
        string += '\t\t\tparticipant_id: {}\n'.format(self.participant_id)
        string += str(self.player)
        return string
 
    def get_participant_id(self):
        return self.participant_id
    def get_player(self):
        return self.player
        
class ParticipantStatsSR:
    def __init__(self, dict):      
		self.assists = dict['assists']
		self.champ_level = dict['champLevel']
		# self.combat_player_score = dict['combatPlayerScore']
		self.deaths = dict['deaths']
		self.double_kills = dict['doubleKills']
		self.first_blood_assist = dict['firstBloodAssist']
		self.first_blood_kill = dict['firstBloodKill']
		self.first_inhibitor_assist = dict['firstInhibitorAssist']
		self.first_inhibitor_kill = dict['firstInhibitorKill']
		self.first_tower_assist = dict['firstTowerAssist']
		self.first_tower_kill = dict['firstTowerKill']
		self.gold_earned = dict['goldEarned']
		self.gold_spent = dict['goldSpent']
		self.inhibitor_kills = dict['inhibitorKills']
		self.item0 = dict['item0']
		self.item1 = dict['item1']
		self.item2 = dict['item2']
		self.item3 = dict['item3']
		self.item4 = dict['item4']
		self.item5 = dict['item5']
		self.item6 = dict['item6']
		self.killing_sprees = dict['killingSprees']
		self.kills = dict['kills']
		self.largest_critical_strike = dict['largestCriticalStrike']
		self.largest_killing_spree = dict['largestKillingSpree']
		self.largest_multi_kill = dict['largestMultiKill']
		self.magic_damage_dealt = dict['magicDamageDealt']
		self.magic_damage_dealt_to_champions = dict['magicDamageDealtToChampions']
		self.magic_damage_taken = dict['magicDamageTaken']
		self.minions_killed = dict['minionsKilled']
		self.neutral_minions_killed = dict['neutralMinionsKilled']
		self.neutral_minions_killed_enemy_jungle = dict['neutralMinionsKilledEnemyJungle']
		self.neutral_minions_killed_team_jungle = dict['neutralMinionsKilledTeamJungle']
		# self.node_capture = dict['nodeCapture']
		# self.node_capture_assist = dict['nodeCaptureAssist']
		# self.node_neutralize = dict['nodeNeutralize']
		# self.node_neutralize_assist = dict['nodeNeutralizeAssist']
		# self.objective_player_score = dict['objectivePlayerScore']
		self.penta_kills = dict['pentaKills']
		self.physical_damage_dealt = dict['physicalDamageDealt']
		self.physical_damage_dealt_to_champions = dict['physicalDamageDealtToChampions']
		self.physical_damage_taken = dict['physicalDamageTaken']
		self.quadra_kills = dict['quadraKills']
		self.sight_wards_bought_in_game = dict['sightWardsBoughtInGame']
		# self.team_objective = dict['teamObjective']
		self.total_damage_dealt = dict['totalDamageDealt']
		self.total_damage_dealt_to_champions = dict['totalDamageDealtToChampions']
		self.total_damage_taken = dict['totalDamageTaken']
		self.total_heal = dict['totalHeal']
		# self.total_player_score = dict['totalPlayerScore']
		# self.total_score_rank = dict['totalScoreRank']
		self.total_time_crowd_control_dealt = dict['totalTimeCrowdControlDealt']
		self.total_units_healed = dict['totalUnitsHealed']
		self.tower_kills = dict['towerKills']
		self.triple_kills = dict['tripleKills']
		self.true_damage_dealt = dict['trueDamageDealt']
		self.true_damage_dealt_to_champions = dict['trueDamageDealtToChampions']
		self.true_damage_taken = dict['trueDamageTaken']
		self.unreal_kills = dict['unrealKills']
		self.vision_wards_bought_in_game = dict['visionWardsBoughtInGame']
		self.wards_killed = dict['wardsKilled']
		self.wards_placed = dict['wardsPlaced']
		self.winner = dict['winner']

class ParticipantTimeline:
    def __init__(self, dict):
        if 'ancientGolemAssistsPerMinCounts' in dict:
            self.ancient_golem_assists_per_min_counts = ParticipantTimelineData(dict['ancientGolemAssistsPerMinCounts'])
        if 'ancientGolemKillsPerMinCounts' in dict:
            self.ancient_golem_kills_per_min_counts = ParticipantTimelineData(dict['ancientGolemKillsPerMinCounts'])
        if 'assistedLaneDeathsPerMinDeltas' in dict:
            self.assisted_lane_deaths_per_min_deltas = ParticipantTimelineData(dict['assistedLaneDeathsPerMinDeltas'])
        if 'assistedLaneKillsPerMinDeltas' in dict:
            self.assisted_lane_kills_per_min_deltas = ParticipantTimelineData(dict['assistedLaneKillsPerMinDeltas'])
        if 'baronAssistsPerMinCounts' in dict:
            self.baron_assists_per_min_counts = ParticipantTimelineData(dict['baronAssistsPerMinCounts'])
        if 'baronKillsPerMinCounts' in dict:
            self.baron_kills_per_min_counts = ParticipantTimelineData(dict['baronKillsPerMinCounts'])
        if 'creepsPerMinDeltas' in dict:
            self.creeps_per_min_deltas = ParticipantTimelineData(dict['creepsPerMinDeltas'])
        if 'csDiffPerMinDeltas' in dict:
            self.cs_diff_per_min_deltas = ParticipantTimelineData(dict['csDiffPerMinDeltas'])
        if 'damageTakenDiffPerMinDeltas' in dict:
            self.damage_taken_diff_per_min_deltas = ParticipantTimelineData(dict['damageTakenDiffPerMinDeltas'])
        if 'damageTakenPerMinDeltas' in dict:
            self.damage_taken_per_min_deltas = ParticipantTimelineData(dict['damageTakenPerMinDeltas'])
        if 'dragonAssistsPerMinCounts' in dict:
            self.dragon_assists_per_min_counts = ParticipantTimelineData(dict['dragonAssistsPerMinCounts'])
        if 'dragonKillsPerMinCounts' in dict:
            self.dragon_kills_per_min_counts = ParticipantTimelineData(dict['dragonKillsPerMinCounts'])
        if 'elderLizardAssistsPerMinCounts' in dict:
            self.elder_lizard_assists_per_min_counts = ParticipantTimelineData(dict['elderLizardAssistsPerMinCounts'])
        if 'elderLizardKillsPerMinCounts' in dict:
            self.elder_lizard_kills_per_min_counts = ParticipantTimelineData(dict['elderLizardKillsPerMinCounts'])
        if 'goldPerMinDeltas' in dict:
            self.gold_per_min_deltas = ParticipantTimelineData(dict['goldPerMinDeltas'])
        if 'inhibitorAssistsPerMinCounts' in dict:
            self.inhibitor_assists_per_min_counts = ParticipantTimelineData(dict['inhibitorAssistsPerMinCounts'])
        if 'inhibitorKillsPerMinCounts' in dict:
            self.inhibitor_kills_per_min_counts = ParticipantTimelineData(dict['inhibitorKillsPerMinCounts'])
        if 'lane' in dict:
            self.lane = dict['lane']
        if 'role' in dict:
            self.role = dict['role']
        if 'towerAssistsPerMinCounts' in dict:
            self.tower_assists_per_min_counts = ParticipantTimelineData(dict['towerAssistsPerMinCounts'])
        if 'towerKillsPerMinCounts' in dict:
            self.tower_kills_per_min_counts = ParticipantTimelineData(dict['towerKillsPerMinCounts'])
        if 'towerKillsPerMinDeltas' in dict:
            self.tower_kills_per_min_deltas = ParticipantTimelineData(dict['towerKillsPerMinDeltas'])
        if 'vilemawAssistsPerMinCounts' in dict:
            self.vilemaw_assists_per_min_counts = ParticipantTimelineData(dict['vilemawAssistsPerMinCounts'])
        if 'vilemawKillsPerMinCounts' in dict:
            self.vilemaw_kills_per_min_counts = ParticipantTimelineData(dict['vilemawKillsPerMinCounts'])
        if 'wardsPerMinDeltas' in dict:
            self.wards_per_min_deltas = ParticipantTimelineData(dict['wardsPerMinDeltas'])
        if 'xpDiffPerMinDeltas' in dict:
            self.xp_diff_per_min_deltas = ParticipantTimelineData(dict['xpDiffPerMinDeltas'])
        if 'xpPerMinDeltas' in dict:
            self.xp_per_min_deltas = ParticipantTimelineData(dict['xpPerMinDeltas'])

    def __str__(self):
        string = ''
        for key in self.__dict__:
            string += '{}: {}\n'.format(key, self.__dict__[key])
        return string
 
    def get_ancient_golem_assists_per_min_counts(self):
        return self.ancient_golem_assists_per_min_counts
    def get_ancient_golem_kills_per_min_counts(self):
        return self.ancient_golem_kills_per_min_counts
    def get_assisted_lane_deaths_per_min_deltas(self):
        return self.assisted_lane_deaths_per_min_deltas
    def get_assisted_lane_kills_per_min_deltas(self):
        return self.assisted_lane_kills_per_min_deltas
    def get_baron_assists_per_min_counts(self):
        return self.baron_assists_per_min_counts
    def get_baron_kills_per_min_counts(self):
        return self.baron_kills_per_min_counts
    def get_creeps_per_min_deltas(self):
        return self.creeps_per_min_deltas
    def get_cs_diff_per_min_deltas(self):
        return self.cs_diff_per_min_deltas
    def get_damage_taken_diff_per_min_deltas(self):
        return self.damage_taken_diff_per_min_deltas
    def get_damage_taken_per_min_deltas(self):
        return self.damage_taken_per_min_deltas
    def get_dragon_assists_per_min_counts(self):
        return self.dragon_assists_per_min_counts
    def get_dragon_kills_per_min_counts(self):
        return self.dragon_kills_per_min_counts
    def get_elder_lizard_assists_per_min_counts(self):
        return self.elder_lizard_assists_per_min_counts
    def get_elder_lizard_kills_per_min_counts(self):
        return self.elder_lizard_kills_per_min_counts
    def get_gold_per_min_deltas(self):
        return self.gold_per_min_deltas
    def get_inhibitor_assists_per_min_counts(self):
        return self.inhibitor_assists_per_min_counts
    def get_inhibitor_kills_per_min_counts(self):
        return self.inhibitor_kills_per_min_counts
    def get_lane(self):
        return self.lane
    def get_role(self):
        return self.role
    def get_tower_assists_per_min_counts(self):
        return self.tower_assists_per_min_counts
    def get_tower_kills_per_min_counts(self):
        return self.tower_kills_per_min_counts
    def get_tower_kills_per_min_deltas(self):
        return self.tower_kills_per_min_deltas
    def get_vilemaw_assists_per_min_counts(self):
        return self.vilemaw_assists_per_min_counts
    def get_vilemaw_kills_per_min_counts(self):
        return self.vilemaw_kills_per_min_counts
    def get_wards_per_min_deltas(self):
        return self.wards_per_min_deltas
    def get_xp_diff_per_min_deltas(self):
        return self.xp_diff_per_min_deltas
    def get_xp_per_min_deltas(self):
        return self.xp_per_min_deltas
        
class ParticipantTimelineData:
    def __init__(self, dict):
        self.ten_to_twenty = dict['tenToTwenty']
        if 'thirtyToEnd' in dict:
            self.thirty_to_end = dict['thirtyToEnd']
        if 'twentyToThirty' in dict:
            self.twenty_to_thirty = dict['twentyToThirty']
        self.zero_to_ten = dict['zeroToTen']    

    def __str__(self):
        string = ''
        for key in self.__dict__:
            string += '{}: {}\n'.format(key, self.__dict__[key])
        return string
            
class PassiveDto:
    def __init__(self, dict):
        self.description = dict['description']
        self.image = ImageDto(dict['image'])
        self.name = dict['name']
        self.sanitized_description = dict['sanitizedDescription']
     
class Player:
    def __init__(self, dict):
        if 'matchHistoryUri' in dict:
            self.match_history_uri = dict['matchHistoryUri']
        if 'profileIcon' in dict:
            self.profile_icon = dict['profileIcon']
        if 'summonerId' in dict:
            self.summoner_id = dict['summonerId']
        if 'summonerName' in dict:
            self.summoner_name = dict['summonerName']
        
    def __str__(self):
        string = ''
        for key in self.__dict__:
            string += '\t\t\t{}: {}\n'.format(key, self.__dict__[key])
        return string
 
    def get_match_history_uri(self):
        return self.match_history_uri
    def get_profile_icon(self):
        return self.profile_icon
    def get_summoner_id(self):
        return self.summoner_id
    def get_summoner_name(self):
        return self.summoner_name
        
class PlayerDto:
    def __init__(self, dict):
        self.champion_id = dict['championId']
        self.summoner_id = dict['summonerId']
        self.team_id = dict['teamId']

class PlayerHistory:
    def __init__(self, dict):
        self.matches = [MatchSummary(el) for el in dict['matches']]
        
    def __str__(self):
        string = ''
        i = 0
        for match in self.matches:
            string += 'Match #{}: \n{}\n'.format(i, match)
            i += 1
        return string
    
class PlayerStatsSummaryDto:
	def __init__(self, dict):
		self.aggregated_stats = AggregatedStatsDto(dict['aggregatedStats'])
		self.losses = dict['losses']
		self.modify_date = dict['modifyDate']
		self.player_stat_summary_type = dict['playerStatSummaryType']
		self.wins = dict['wins']
    
class PlayerStatsSummaryListDto:
	def __init__(self, dict):
		self.player_stat_summaries = [PlayerStatsSummaryDto(el) for el in dict['playerStatSummaries']]
		self.summoner_id = dict['summonerId']
      
class Position:
    def __init__(self, dict):
        self.x = dict['x']
        self.y = dict['y']

# Contains aggregated ranked stats by champion for a given summoner        
class RankedStatsDto:
	def __init__(self, dict):
		self.champions = [ChampionStatsDto(el) for el in dict['champions']]
		self.modify_date = dict['modifyDate']
		self.summoner_id = dict['summonerId']
        
class RawStatsDto:
    def __init__(self, dict):
        self.assists = dict['assists']
        self.barracks_killed = dict['barracksKilled']
        self.champions_killed = dict['championsKilled']
        self.combat_player_score = dict['combatPlayerScore']
        self.consumables_purchased = dict['consumablesPurchased']
        self.damage_dealt_player = dict['damageDealtPlayer']
        self.double_kills = dict['doubleKills']
        self.first_blood = dict['firstBlood']
        self.gold = dict['gold']
        self.gold_earned = dict['goldEarned']
        self.gold_spent = dict['goldSpent']
        self.item0 = dict['item0']
        self.item1 = dict['item1']
        self.item2 = dict['item2']
        self.item3 = dict['item3']
        self.item4 = dict['item4']
        self.item5 = dict['item5']
        self.item6 = dict['item6']
        self.items_purchased = dict['itemsPurchased']
        self.killing_sprees = dict['killingSprees']
        self.largest_critical_strike = dict['largestCriticalStrike']
        self.largest_killing_spree = dict['largestKillingSpree']
        self.largest_multi_kill = dict['largestMultiKill']
        self.legendary_items_created = dict['legendaryItemsCreated']
        self.level = dict['level']
        self.magic_damage_dealt_player = dict['magicDamageDealtPlayer']
        self.magic_damage_dealt_to_champions = dict['magicDamageDealtToChampions']
        self.magic_damage_taken = dict['magicDamageTaken']
        self.minions_denied = dict['minionsDenied']
        self.minions_killed = dict['minionsKilled']
        self.neutral_minions_killed = dict['neutralMinionsKilled']
        self.neutral_minions_killed_enemy_jungle = dict['neutralMinionsKilledEnemyJungle']
        self.neutral_minions_killed_your_jungle = dict['neutralMinionsKilledYourJungle']
        self.nexus_killed = dict['nexusKilled']
        self.node_capture = dict['nodeCapture']
        self.node_capture_assist = dict['nodeCaptureAssist']
        self.node_neutralize = dict['nodeNeutralize']
        self.node_neutralize_assist = dict['nodeNeutralizeAssist']
        self.num_deaths = dict['numDeaths']
        self.num_items_bought = dict['numItemsBought']
        self.objective_player_score = dict['objectivePlayerScore']
        self.penta_kills = dict['pentaKills']
        self.physical_damage_dealt_player = dict['physicalDamageDealtPlayer']
        self.physical_damage_dealt_to_champions = dict['physicalDamageDealtToChampions']
        self.physical_damage_taken = dict['physicalDamageTaken']
        self.player_position = dict['playerPosition']
        self.player_role = dict['playerRole']
        self.quadra_kills = dict['quadraKills']
        self.sight_wards_bought = dict['sightWardsBought']
        self.spell1_cast = dict['spell1Cast']
        self.spell2_cast = dict['spell2Cast']
        self.spell3_cast = dict['spell3Cast']
        self.spell4_cast = dict['spell4Cast']
        self.summon_spell1_cast = dict['summonSpell1Cast']
        self.summon_spell2_cast = dict['summonSpell2Cast']
        self.super_monster_killed = dict['superMonsterKilled']
        self.team = dict['team']
        self.team_objective = dict['teamObjective']
        self.time_played = dict['timePlayed']
        self.total_damage_dealt = dict['totalDamageDealt']
        self.total_damage_dealt_to_champions = dict['totalDamageDealtToChampions']
        self.total_damage_taken = dict['totalDamageTaken']
        self.total_heal = dict['totalHeal']
        self.total_player_score = dict['totalPlayerScore']
        self.total_score_rank = dict['totalScoreRank']
        self.total_time_crowd_control_dealt = dict['totalTimeCrowdControlDealt']
        self.total_units_healed = dict['totalUnitsHealed']
        self.triple_kills = dict['tripleKills']
        self.true_damage_dealt_player = dict['trueDamageDealtPlayer']
        self.true_damage_dealt_to_champions = dict['trueDamageDealtToChampions']
        self.true_damage_taken = dict['trueDamageTaken']
        self.turrets_killed = dict['turretsKilled']
        self.unreal_kills = dict['unrealKills']
        self.victory_point_total = dict['victoryPointTotal']
        self.vision_wards_bought = dict['visionWardsBought']
        self.ward_killed = dict['wardKilled']
        self.ward_placed = dict['wardPlaced']
        self.win = dict['win']       
    
class RealmDto:
    def __init__(self, dict):
		self.cdn = dict['cdn']
		self.css = dict['css']
		self.dd = dict['dd']
		self.l = dict['l']
		self.lg = dict['lg']
		self.n = dict['n']
		self.profile_icon_max = dict['profileiconmax']
		self.store = dict['store']
		self.v = dict['v']    

# Contains 0-10 recent games played by a given summoner        
class RecentGamesDto:
    def __init__(self, dict):
        self.games = set()
        for game in dict['games']:
            self.games.append(GameDto(game))
        self.summoner_id = dict['summonerId']
     
class RecommendedDto:
    def __init__(self, dict):
        self.blocks = [BlockDto(block) for block in dict['blocks']]
        self.champion = dict['champion']
        self.map = dict['map']
        self.mode = dict['mode']
        self.priority = dict['priority']
        self.title = dict['title']
        self.type = dict['type']
     
class RosterDto:
	def __init__(self, dict):
		self.member_list = [TeamMemberInfoDto(el) for el in dict['memberList']]
		self.owner_id = dict['ownerId']
     
class Rune:
    def __init__(self, dict):
        self.rank = dict['rank']
        self.rune_id = dict['runeId']

class RuneDto:
    def __init__(self, dict):
        self.colloq = dict['colloq']
        self.consume_on_full = dict['consumeOnFull']
        self.consumed = dict['consumed']
        self.depth = dict['depth']
        self.description = dict['description']
        self.frum = dict['from']
        self.gold = GoldDto(dict['gold'])
        self.group = dict['group']
        self.hide_from_all = dict['hideFromAll']
        self.id = dict['id']
        self.image = ImageDto(dict['image'])
        self.in_store = dict['inStore']
        self.into = dict['into']
        self.maps = dict['maps']
        self.name = dict['name'] 
        self.plaintext = dict['plaintext']
        self.required_champion = dict['requiredChampion']
        self.rune = MetaDataDto(dict['rune'])
        self.sanitized_description = dict['sanitizedDescription']
        self.special_recipe = dict['specialRecipe']
        self.stacks = dict['stacks']
        self.stats = BasicDataStatsDto(dict['stats'])
        self.tags = dict['tags']        
        
class RuneListDto:
    def __init__(self, dict):
        self.basic = BasicDataDto(dict['basic'])
        self.data = {}
        for key in dict['data']:
            self.data[key] = RuneDto(dict['data'][key])
        self.type = dict['type']
        self.version = dict['version']

class RunePageDto:
	def __init__(self, dict):
		self.current = dict['current']
		self.id = dict['id']
		self.name = dict['name']
		self.slots = Set[RuneSlotDto](dict['slots'])
    
class RunePagesDto:
	def __init__(self, dict):
		self.pages = Set[RunePageDto](dict['pages'])
		self.summoner_id = dict['summonerId']
    
class RuneSlotDto:
	def __init__(self, dict):
		self.rune_id = dict['runeId']
		self.rune_slot_id = dict['runeSlotId']
    
class Service:
    def __init__(self, dict):
        self.incidents = [Incident(el) for el in dict['incidents']]
        self.name = dict['name']
        self.slug = dict['slug']
        self.status = dict['status']
    
class Shard:
    def __init__(self,dict):
		self.hostname = dict['hostname']
		self.locales = dict['locales']
		self.name = dict['name']
		self.region_tag = dict['region_tag']
		self.slug = dict['slug']    

class ShardStatus:
    def __init__(self, dict):
        self.hostname = dict['hostname']
        self.locales = dict['locales']
        self.name = dict['name']
        self.region_tag = dict['region_tag']
        self.services = [Service(el) for el in dict['services']]
        self.slug = dict['slug'] 
        
class SkinDto:
    def __init__(self, dict):
        self.id = dict['id']
        self.name = dict['name']
        self.num = dict['num']
      
class SpellVarsDto:
    def __init__(self, dict):
        self.coeff = dict['coeff']
        self.dyn = dict['dyn']
        self.key = dict['key']
        self.link = dict['link']
        self.ranks_with = dict['ranksWith']
      
class StatsDto:
    def __init__(self, dict):
        self.armor = dict['armor']
        self.armor_per_level = dict['armorperlevel']
        self.attack_damage = dict['attackdamage']
        self.attack_damage_per_level = dict['attackdamageperlevel']		
        self.attack_range = dict['attackrange']		
        self.attack_speed_offset = dict['attackspeedoffset']		
        self.attack_speed_per_level = dict['attackspeedperlevel']		
        self.crit = dict['crit']		
        self.crit_per_level = dict['critperlevel']		
        self.hp = dict['hp']		
        self.hp_per_level = dict['hpperlevel']		
        self.hp_regen = dict['hpregen']		
        self.hp_regen_per_level = dict['hpregenperlevel']		
        self.movespeed = dict['movespeed']	
        self.mp = dict['mp']		
        self.mp_per_level = dict['mpperlevel']		
        self.mp_regen = dict['mpregen']		
        self.mp_regen_per_level = dict['mpregenperlevel']		
        self.spellblock = dict['spellblock']		
        self.spellblock_per_level = dict['spellblockperlevel']		
        
class SummonerDto:
    def __init__(self, dict):
        dict = dict.items()[0][1]

        self.id = dict['id']
        self.name = dict['name']
        self.profile_icon_id = dict['profileIconId']
        self.revision_date = dict['revisionDate']
        self.summoner_level = dict['summonerLevel']
        
    def __str__(self):
        return 'id = {}\nname = {}'.format(self.id, self.name)
    
    def summoner_by_name(self, *sumname):
        region = 'na'
        sumname = 'Eater%20of%20Chicken'
        url = 'https://na.api.pvp.net/api/lol/' + region 
        url += '/v1.4/summoner/by-name/'+ sumname + '?api_key=' + api_key

        response = urllib2.urlopen(url)
        html = response.read()

class SummonerSpellDto:
    def __init__(self, dict):
		self.cooldown = dict['cooldown']
		self.cooldown_burn = dict['cooldownBurn']
		self.cost = dict['cost']
		self.cost_burn = dict['costBurn']
		self.cost_type = dict['costType']
		self.description = dict['description']
		self.effect = dict['effect']
		self.effect_burn = dict['effectBurn']
		self.id = dict['id']
		self.image = ImageDto(dict['image'])
		self.key = dict['key']
		self.leveltip = LevelTipDto(dict['leveltip'])
		self.maxrank = dict['maxrank']
		self.modes = dict['modes']
		self.name = dict['name']
		self.range = dict['range']
		self.range_burn = dict['rangeBurn']
		self.resource = dict['resource']
		self.sanitized_description = dict['sanitizedDescription']
		self.sanitized_tooltip = dict['sanitizedTooltip']
		self.summoner_level = dict['summonerLevel']
		self.tooltip = dict['tooltip']
		self.vars = [SpellVarsDto(el) for el in dict['vars']]    
                    
class SummonerSpellListDto:
    def __init__(self, dict):
        self.data = {}
        for key in dict['data']:
            self.data[key] = dict['data'][key]
        self.type = dict['type']
        self.version = dict['version']

class Team:
    def __init__(self, dict):
		self.bans = [BannedChampion(el) for el in dict['bans']]
		self.baron_kills = dict['baronKills']
		self.dominion_victory_score = dict['dominionVictoryScore']
		self.dragon_kills = dict['dragonKills']
		self.first_baron = dict['firstBaron']
		self.first_blood = dict['firstBlood']
		self.first_dragon = dict['firstDragon']
		self.first_inhibitor = dict['firstInhibitor']
		self.first_tower = dict['firstTower']
		self.inhibitor_kills = dict['inhibitorKills']
		self.team_id = dict['teamId']
		self.tower_kills = dict['towerKills']
		self.vilemaw_kills = dict['vilemawKills']
		self.winner = dict['winner']       
   
class TeamDto:
	def __init__(self, dict):
		self.create_date = dict['createDate']
		self.full_id = dict['fullId']
		self.last_game_date = dict['lastGameDate']
		self.last_join_date = dict['lastJoinDate']
		self.last_joined_ranked_team_queue_date = dict['lastJoinedRankedTeamQueueDate']
		self.match_history = [MatchHistorySummaryDto(el) for el in dict['matchHistory']]
		self.modify_date = dict['modifyDate']
		self.name = dict['name']
		self.roster = RosterDto(dict['roster'])
		self.second_last_join_date = dict['secondLastJoinDate']
		self.status = dict['status']
		self.tag = dict['tag']
		self.team_stat_details = [TeamStatDetailDto(el) for el in dict['teamStatDetails']]
		self.third_last_join_date = dict['thirdLastJoinDate']
   
class TeamMemberInfoDto:
	def __init__(self, dict):
		self.invite_date = dict['inviteDate']
		self.join_date = dict['joinDate']
		self.player_id = dict['playerId']
		self.status = dict['status']
   
class TeamStatDetailDto:
	def __init__(self, dict):
		self.average_games_played = dict['averageGamesPlayed']
		self.losses = dict['losses']
		self.team_stat_type = dict['teamStatType']
		self.wins = dict['wins']
   
class Timeline:
    def __init__(self, dict):
        self.frame_interval = dict['frameInterval']
        self.frames = [Frame(el) for el in dict['frames']]
       
class Translation:
    def __init__(self, dict):
        self.content = dict['content']
        self.locale = dict['locale']
        self.updated_at = dict['updated_at']
   
   