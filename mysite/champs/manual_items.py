class Item:
    def __init__(self, id, children=[], parents=[]):
        self.id = id
        self.children = []
        for child in children:
            self.children.append(child)
            if self not in child.parents:
                child.parents.append(self)
        self.parents = []
        for parent in parents:
            self.parents.append(parent)
            parent.children.append(self)
    
    def __str__(self):
        string = 'ID: {id}'.format(id=self.id)
        for child in self.children:
            string += '\n\t{child}'.format(child=str(child))
  
        return string
                
    def is_basic(self):
        return not self.children
    
    def is_advanced(self):
        if not self.is_basic():
            for child in self.children:
                if not child.is_basic():
                    return False
            return True
        else: 
            return False
    
    def is_legendary(self):
        if not self.is_advanced() and not self.is_basic():
            for child in self.children:
                if not (child.is_advanced() or child.is_basic()):
                    return False
            return True
        else: 
            return False
    
    def is_mythical(self):
        return not (self.is_basic() or self.is_advanced() or self.is_legendary())
    
    def is_component(self):
        return not self.parents
            
    def add_parent(self, other):
        if type(other) is list:
            for item in other:
                other.children.append(self)
                self.parents.append(item)
        else:
            other.children.append(self)
            self.parents.append(other)
        
    def add_child(self, other):
        if type(other) is list:
            for item in other:
                self.children.append(other)
        else:
            self.children.append(other)

tome = Item(1052)
coin = Item(3301)
bf = Item(1038)
wand = Item(1026)
boots = Item(1001)
gloves = Item(1051)
cloak = Item(1018)
cloth = Item(1029)
dagger = Item(1042)
d_blade = Item(1055)
d_ring = Item(1056)
d_shield = Item(1054)
charm = Item(1004)
machete = Item(1039)
long_sword = Item(1036)
rod = Item(1058)
mantle = Item(1033)
pickaxe = Item(1037)
bead = Item(1006)
relic = Item(3302)
ruby = Item(1028)
sapphire = Item(1027)
spellthiefs = Item(3303)

aegis = Item(3105, children=[bead, ruby, mantle])
aether = Item(3113, children=[tome])
avarice = Item(3093, children=[gloves])
belt = Item(1011, children=[ruby])
berserkers = Item(3006, children=[boots, dagger])
bow = Item(1043, children=[dagger, dagger])
bracer = Item(3801, children=[ruby, bead])
brutalizer = Item(3134, children=[long_sword, long_sword])
catalyst = Item(3010, children=[ruby, sapphire])
chain_vest = Item(1031, children=[cloth])
chalice = Item(3028, children=[mantle, charm, charm])
cinder = Item(3751, children=[ruby])
codex = Item(3108, children=[tome])
cowl = Item(3211, children=[ruby, mantle])
frostfang = Item(3098, children=[spellthiefs])
guise = Item(3136, children=[ruby, tome])
hexdrinker = Item(3155, children=[long_sword, mantle])
idol = Item(3114, children=[charm, charm])
ie = Item(3031, children=[bf, cloak, pickaxe])
kindlegem = Item(3067, children=[ruby])
lucidity = Item(3158, children=[boots])
lw = Item(3035, children=[long_sword, pickaxe])
medallion = Item(3096, children=[coin])
mejais = Item(3041, children=[tome])
mercs = Item(3111, children=[boots, mantle])
mobis = Item(3117, children=[boots])
negatron = Item(1057, children=[mantle])
phage = Item(3044, children=[ruby, long_sword])
poachers = Item(3711, children=[machete])
qss = Item(3140, children=[mantle])
rabadons = Item(3089, children=[rod, wand, tome])
rageblade = Item(3124, children=[pickaxe, wand])
rangers = Item(3713, children=[machete])
raptor = Item(2053, children=[bead, cloth])
revolver = Item(3145, children=[tome, tome])
seekers = Item(3191, children=[cloth, tome])
sheen = Item(3057, children=[sapphire, tome])
shroud = Item(3024, children=[sapphire, cloth])
sightstone = Item(2049, children=[ruby])
skirmishers = Item(3715, children=[machete])
sorcs = Item(3020, children=[boots])
stalkers = Item(3706, children=[machete])
stinger = Item(3101, children=[dagger, dagger])
swifties = Item(3009, children=[boots])
sword_occult = Item(3141, children=[long_sword])
tabis = Item(3047, children=[boots, cloth])
targons = Item(3097, children=[relic])
tear = Item(3070, children=[sapphire, charm])
tiamat = Item(3077, children=[pickaxe, long_sword, bead, bead])
vamp = Item(1053, children=[long_sword])
void = Item(3135, children=[tome, wand])
wardens = Item(3082, children=[cloth, cloth])
wits_end = Item(3091, children=[dagger, bow, mantle])
zeal = Item(3086, children=[dagger, gloves])

stalkers_warrior = Item(3707, children=[stalkers])
stalkers_runeglaive = Item(3708, children=[stalkers])
stalkers_cinderhulk = Item(3709, children=[stalkers])
stalkers_devourer = Item(3710, children=[stalkers])
stalkers_sated = Item(3930, children=[stalkers_devourer])

skirmishers_warrior = Item(3714, children=[skirmishers])
skirmishers_runeglaive = Item(3716, children=[skirmishers])
skirmishers_cinderhulk = Item(3717, children=[skirmishers])
skirmishers_devourer = Item(3718, children=[skirmishers])
skirmishers_sated = Item(3930, children=[skirmishers_devourer])

poachers_warrior = Item(3719, children=[poachers])
poachers_runeglaive = Item(3720, children=[poachers])
poachers_cinderhulk = Item(3721, children=[poachers])
poachers_devourer = Item(3722, children=[poachers])
poachers_sated = Item(3932, children=[poachers_devourer])

rangers_warrior = Item(3723, children=[rangers])
rangers_runeglaive = Item(3724, children=[rangers])
rangers_cinderhulk = Item(3725, children=[rangers])
rangers_devourer = Item(3726, children=[rangers])
rangers_sated = Item(3933, children=[rangers_devourer])

berserkers_furor = Item(1300, children=[berserkers])
berserkers_alacrity = Item(1301, children=[berserkers])
berserkers_captain = Item(1302, children=[berserkers])
berserkers_distortion = Item(1303, children=[berserkers])
berserkers_homeguard = Item(1304, children=[berserkers])

swifties_furor = Item(1305, children=[swifties])
swifties_alacrity = Item(1306, children=[swifties])
swifties_captain = Item(1307, children=[swifties])
swifties_distortion = Item(1308, children=[swifties])
swifties_homeguard = Item(1309, children=[swifties])

sorcs_furor = Item(1310, children=[sorcs])
sorcs_alacrity = Item(1311, children=[sorcs])
sorcs_captain = Item(1312, children=[sorcs])
sorcs_distortion = Item(1313, children=[sorcs])
sorcs_homeguard = Item(1314, children=[sorcs])

tabis_furor = Item(1315, children=[tabis])
tabis_alacrity = Item(1316, children=[tabis])
tabis_captain = Item(1317, children=[tabis])
tabis_distortion = Item(1318, children=[tabis])
tabis_homeguard = Item(1319, children=[tabis])

mercs_furor = Item(1320, children=[mercs])
mercs_alacrity = Item(1321, children=[mercs])
mercs_captain = Item(1322, children=[mercs])
mercs_distortion = Item(1323, children=[mercs])
mercs_homeguard = Item(1324, children=[mercs])

mobis_furor = Item(1325, children=[mobis])
mobis_alacrity = Item(1326, children=[mobis])
mobis_captain = Item(1327, children=[mobis])
mobis_distortion = Item(1328, children=[mobis])
mobis_homeguard = Item(1329, children=[mobis])

lucidity_furor = Item(1330, children=[lucidity])
lucidity_alacrity = Item(1331, children=[lucidity])
lucidity_captain = Item(1332, children=[lucidity])
lucidity_distortion = Item(1333, children=[lucidity])
lucidity_homeguard = Item(1334, children=[lucidity])

abyssal = Item(3001, children=[wand, negatron])
archangels = Item(3003, children=[tear, wand])
athenes = Item(3174, children=[chalice, codex])
banner = Item(3060, children=[aegis, codex])
banshees = Item(3102, children=[cowl, ruby])
bt = Item(3072, children=[vamp, bf])
censer = Item(3504, children=[idol, aether])
cleaver = Item(3071, children=[phage, kindlegem])
cutlass = Item(3144, children=[vamp, long_sword])
dead_mans = Item(3742, children=[chain_vest, belt])
er = Item(3508, children=[bt, vamp])
face = Item(3401, children=[targons, kindlegem])
frost_queens = Item(3092, children=[frostfang, codex])
fh = Item(3110, children=[wardens, shroud])
fromal = Item(3022, children=[pickaxe, belt, ruby])
ga = Item(3026, children=[negatron, chain_vest])
iceborn = Item(3025, children=[sheen, shroud])
liandrys = Item(3151, children=[guise, tome])
lich = Item(3100, children=[sheen, aether])
locket = Item(3190, children=[aegis, kindlegem])
ludens = Item(3285, children=[rod, aether])
manamune = Item(3004, children=[tear, pickaxe])
maw = Item(3156, children=[hexdrinker, pickaxe])
mercurial = Item(3139, children=[qss, bf])
mikaels = Item(3222, children=[chalice, idol])
morellos = Item(3165, children=[codex, idol])
nashors = Item(3115, children=[stinger, codex])
ohmwrecker = Item(3056, children=[raptor, kindlegem])
pd = Item(3046, children=[zeal, cloak, dagger])
randuins = Item(3143, children=[wardens, belt])
rg = Item(3800, children=[catalyst, bracer])
r_hydra = Item(3074, children=[tiamat, vamp])
roa = Item(3027, children=[catalyst, wand])
ruby_sightstone = Item(2045, children=[ruby, sightstone])
runaans = Item(3085, children=[bow, dagger, dagger])
rylais = Item(3116, children=[wand, tome, belt])
shiv = Item(3087, children=[zeal, avarice])
steraks = Item(3053, children=[belt, long_sword])
sunfire = Item(3068, children=[chain_vest, cinder])
sv = Item(3065, children=[cowl, kindlegem])
talisman = Item(3069, children=[medallion, idol])
t_hydra = Item(3748, children=[tiamat, belt])
thornmail = Item(3075, children=[cloth, chain_vest])
triforce = Item(3078, children=[zeal, phage, sheen])
twin_shadows = Item(3023, children=[codex, aether])
warmogs = Item(3083, children=[bracer, bracer, belt])
wota = Item(3152, children=[revolver, codex])
youmuus = Item(3142, children=[avarice, brutalizer])
z_harbinger = Item(3050, children=[shroud, tome, tome])
zephyr = Item(3172, children=[stinger, pickaxe])
zhonyas = Item(3157, children=[seekers, rod])
zzrot = Item(3512, children=[raptor, negatron])

bork = Item(3153, children=[cutlass, bow])
gunblade = Item(3146, children=[revolver, cutlass])
muramana = Item(3042, children=[manamune])
seraphs = Item(3040, children=[archangels])

hex_core_0 = Item(3200)
hex_core_1 = Item(3196, children=[hex_core_0])
hex_core_2 = Item(3197, children=[hex_core_1])
hex_core_3 = Item(3198, children=[hex_core_2])
      
black_spear = Item(3599)

pot = Item(2003)
blue_pot = Item(2004)
biscuit = Item(2010)
flask = Item(2041)
pink = Item(2043)
green = Item(2044)
ruin = Item(2137)
iron = Item(2138)
sorcery = Item(2139)
wrath = Item(2140)
      
yellow_t = Item(3340)
yellow_yellow_t = Item(3361, children=[yellow_t])
pink_yellow_t = Item(3362, children=[yellow_t])

blue_t = Item(3342)
blue_blue_t = Item(3363, children=[blue_t])

red_t = Item(3341)
red_red_t = Item(3364, children=[red_t])

gp_rate_up = Item(3901)
gp_true = Item(3902)
gp_allies = Item(3903)