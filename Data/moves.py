class BASIC_MOVE:
    ID = 0
    Name = 1
    Type = 2
    PW = 3
    Duration = 4
    NRG = 5
    NRGPS = 6
    DPS = 7

BASIC_MOVE_DATA = [
    # ID, Name,Type, PW, Duration (ms), NRG, NRGPS, DPS
    [200,"Fury Cutter","Bug",3,400,6,15,7.50],
    [201,"Bug Bite","Bug",5,450,7,15.56,11.11],
    [202,"Bite","Dark",6,500,7,14,12.00],
    [203,"Sucker Punch","Dark",7,700,9,12.86,10.00],
    [204,"Dragon Breath","Dragon",6,500,7,14,12.00],
    [205,"Thunder Shock","Electric",5,600,8,13.33,8.33],
    [206,"Spark","Electric",7,700,8,11.43,10.00],
    [207,"Low Kick","Fighting",5,600,7,11.67,8.33],
    [208,"Karate Chop","Fighting",6,800,8,10,7.50],
    [209,"Ember","Fire",10,1050,10,9.52,9.52],
    [210,"Wing Attack","Flying",9,750,7,9.33,12.00],
    [211,"Peck","Flying",10,1150,10,8.7,8.70],
    [212,"Lick","Ghost",5,500,6,12,10.00],
    [213,"Shadow Claw","Ghost",11,950,8,8.42,11.58],
    [214,"Vine Whip","Grass",7,650,7,10.77,10.77],
    [215,"Razor Leaf","Grass",15,1450,12,8.28,10.34],
    [216,"Mud Shot","Ground",6,550,7,12.73,10.91],
    [217,"Ice Shard","Ice",15,1400,12,8.57,10.71],
    [218,"Frost Breath","Ice",9,810,7,8.64,11.11],
    [219,"Quick Attack","Normal",10,1330,12,9.02,7.52],
    [220,"Scratch","Normal",6,500,7,14,12.00],
    [221,"Tackle","Normal",12,1100,10,9.09,10.91],
    [222,"Pound","Normal",7,540,7,12.96,12.96],
    [223,"Cut","Normal",12,1130,10,8.85,10.62],
    [224,"Poison Jab","Poison",12,1050,10,9.52,11.43],
    [225,"Acid","Poison",10,1050,10,9.52,9.52],
    [226,"Psycho Cut","Psychic",7,570,7,12.28,12.28],
    [227,"Rock Throw","Rock",12,1360,15,11.03,8.82],
    [228,"Metal Claw","Steel",8,630,7,11.11,12.70],
    [229,"Bullet Punch","Steel",10,1200,10,8.33,8.33],
    [230,"Water Gun","Water",6,500,7,14,12.00],
    [231,"Splash","Water",0,1230,10,8.13,0.00],
    [232,"Water Gun (Blastoise)","Water",6,500,7,14,12.00],
    [233,"Mud Slap","Ground",15,1350,12,8.89,11.11],
    [234,"Zen Headbutt","Psychic",12,1050,9,8.57,11.43],
    [235,"Confusion","Psychic",15,1510,14,9.27,9.93],
    [236,"Poison Sting","Poison",6,575,8,13.91,10.43],
    [237,"Bubble","Water",25,2300,25,10.87,10.87],
    [238,"Feint Attack","Dark",12,1040,10,9.62,11.54],
    [239,"Steel Wing","Steel",15,1330,12,9.02,11.28],
    [240,"Fire Fang","Fire",10,840,8,9.52,11.90],
    [241,"Rock Smash","Fighting",15,1410,12,8.51,10.64],
    [242,"Transform","Normal",0,1200,7,5.83,0.5], # CREATED MANUALLY, BASICALLY MADE UP, PROBABLY ALL WRONG 
]
def _get_basic_move_by_name(name):
    for mv in BASIC_MOVE_DATA:
        if name == mv[BASIC_MOVE.Name]:
            return mv
    return None


class CHARGE_MOVE:
    ID = 0
    Name = 1
    Type = 2
    PW = 3
    Duration = 4
    Crit = 5
    NRG = 6
    
CHARGE_MOVE_DATA = [
    # ID    Name    Type    PW  Duration (ms)   Crit%   NRG Cost
    [13,"Wrap","Normal",25,4000,5,20],
    [14,"Hyper Beam","Dark",120,5000,5,100],
    [16,"Dark Pulse","Poison",45,3500,5,33],
    [18,"Sludge","Normal",30,2600,5,25],
    [20,"Vice Grip","Fire",25,2100,5,20],
    [21,"Flame Wheel","Bug",40,4600,5,25],
    [22,"Megahorn","Fire",80,3200,5,100],
    [24,"Flamethrower","Ground",55,2900,5,50],
    [26,"Dig","Fighting",70,5800,5,33],
    [28,"Cross Chop","Psychic",60,2000,25,100],
    [30,"Psybeam","Ground",40,3800,5,25],
    [31,"Earthquake","Rock",100,4200,5,100],
    [32,"Stone Edge","Ice",80,3100,50,100],
    [33,"Ice Punch","Psychic",45,3500,5,33],
    [34,"Heart Stamp","Electric",25,2550,5,25],
    [35,"Discharge","Steel",35,2500,5,33],
    [36,"Flash Cannon","Flying",60,3900,5,33],
    [38,"Drill Peck","Ice",40,2700,5,33],
    [39,"Ice Beam","Ice",65,3650,5,50],
    [40,"Blizzard","Fire",100,3900,5,100],
    [42,"Heat Wave","Flying",80,3800,5,100],
    [45,"Aerial Ace","Ground",30,2900,5,25],
    [46,"Drill Run","Grass",50,3400,25,33],
    [47,"Petal Blizzard","Grass",65,3200,5,50],
    [48,"Mega Drain","Bug",25,3200,5,20],
    [49,"Bug Buzz","Poison",75,4250,5,50],
    [50,"Poison Fang","Dark",25,2400,5,20],
    [51,"Night Slash","Water",30,2700,25,25],
    [53,"Bubble Beam","Fighting",30,2900,5,25],
    [54,"Submission","Fighting",30,2100,5,33],
    [56,"Low Sweep","Water",30,2250,5,25],
    [57,"Aqua Jet","Water",25,2350,5,20],
    [58,"Aqua Tail","Grass",45,2350,5,50],
    [59,"Seed Bomb","Psychic",40,2400,5,33],
    [60,"Psyshock","Rock",40,2700,5,33],
    [62,"Ancient Power","Rock",35,3600,5,25],
    [63,"Rock Tomb","Rock",30,3400,25,25],
    [64,"Rock Slide","Rock",50,3200,5,33],
    [65,"Power Gem","Ghost",40,2900,5,33],
    [66,"Shadow Sneak","Ghost",25,3100,5,20],
    [67,"Shadow Punch","Ghost",25,2100,5,25],
    [69,"Ominous Wind","Ghost",30,3100,5,25],
    [70,"Shadow Ball","Steel",45,3080,5,33],
    [72,"Magnet Bomb","Steel",30,2800,5,25],
    [74,"Iron Head","Electric",30,2000,5,33],
    [75,"Parabolic Charge","Electric",25,2100,5,20],
    [77,"Thunder Punch","Electric",40,2400,5,33],
    [78,"Thunder","Electric",100,4300,5,100],
    [79,"Thunderbolt","Dragon",55,2700,5,50],
    [80,"Twister","Dragon",25,2700,5,20],
    [82,"Dragon Pulse","Dragon",65,3600,5,50],
    [83,"Dragon Claw","Fairy",35,1500,25,50],
    [84,"Disarming Voice","Fairy",25,3900,5,20],
    [85,"Draining Kiss","Fairy",25,2800,5,20],
    [86,"Dazzling Gleam","Fairy",55,4200,5,33],
    [87,"Moonblast","Fairy",85,4100,5,100],
    [88,"Play Rough","Poison",55,2900,5,50],
    [89,"Cross Poison","Poison",25,1500,25,25],
    [90,"Sludge Bomb","Poison",55,2600,5,50],
    [91,"Sludge Wave","Poison",70,3400,5,100],
    [92,"Gunk Shot","Ground",65,3000,5,100],
    [94,"Bone Club","Ground",25,1600,5,25],
    [95,"Bulldoze","Ground",35,3400,5,25],
    [96,"Mud Bomb","Bug",30,2600,5,25],
    [99,"Signal Beam","Bug",45,3100,5,33],
    [100,"X-Scissor","Fire",35,2100,5,33],
    [101,"Flame Charge","Fire",25,3100,5,20],
    [102,"Flame Burst","Fire",30,2100,5,25],
    [103,"Fire Blast","Water",100,4100,5,100],
    [104,"Brine","Water",25,2400,5,25],
    [105,"Water Pulse","Water",35,3300,5,25],
    [106,"Scald","Water",55,4000,5,33],
    [107,"Hydro Pump","Psychic",90,3800,5,100],
    [108,"Psychic","Psychic",55,2800,5,50],
    [109,"Psystrike","Ice",100,5100,5,100],
    [111,"Icy Wind","Grass",25,3800,5,20],
    [114,"Giga Drain","Fire",50,3600,5,33],
    [115,"Fire Punch","Grass",40,2800,5,33],
    [116,"Solar Beam","Grass",120,4900,5,100],
    [117,"Leaf Blade","Grass",55,2800,25,50],
    [118,"Power Whip","Flying",70,2800,0,100],
    [121,"Air Cutter","Flying",30,3300,25,25],
    [122,"Hurricane","Fighting",80,3200,5,100],
    [123,"Brick Break","Normal",30,1600,25,33],
    [125,"Swift","Normal",30,3000,5,25],
    [126,"Horn Attack","Normal",25,2200,5,25],
    [127,"Stomp","Normal",30,2100,5,25],
    [129,"Hyper Fang","Normal",35,2100,5,33],
    [131,"Body Slam","Normal",40,1560,5,50],
    [132,"Rest","Normal",35,3100,0,33],
    [133,"Struggle","Water",15,1695,0,20],
    [134,"Scald (Blastoise)","Water",55,4000,5,33],
    [135,"Hydro Pump (Blastoise)","Normal",90,3800,5,100],
    [136,"Wrap (Green)","Normal",25,3700,5,20],
    [137,"Wrap (Pink)","Normal",25,3700,5,20],
]
def _get_charge_move_by_name(name):
    for mv in CHARGE_MOVE_DATA:
        if name == mv[CHARGE_MOVE.Name]:
            return mv
    return None


