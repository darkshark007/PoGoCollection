class BASIC_MOVE:
    ID = 0
    Name = 1
    Type = 2
    PW = 3
    Duration = 4
    NRG = 5
    NRGPS = 6
    DPS = 7

# Adapted from the GAME_MASTER_FILE Json Output at:
# https://github.com/pokemongo-dev-contrib/pokemongo-game-master/
# https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/GAME_MASTER.json
BASIC_MOVE_DATA = [
    # ID, Name,Type, PW, Duration (ms), NRG, NRGPS, DPS
    [200,"Fury Cutter","Bug",3,400,6,15,7.5],
    [201,"Bug Bite","Bug",5,500,6,12,10],
    [202,"Bite","Dark",6,500,4,8,12],
    [203,"Sucker Punch","Dark",7,700,8,11.428571428571429,10],
    [204,"Dragon Breath","Dragon",6,500,4,8,12],
    [205,"Thunder Shock","Electric",5,600,8,13.333333333333334,8.333333333333334],
    [206,"Spark","Electric",6,700,9,12.857142857142858,8.571428571428571],
    [207,"Low Kick","Fighting",6,600,6,10,10],
    [208,"Karate Chop","Fighting",8,800,10,12.5,10],
    [209,"Ember","Fire",10,1000,10,10,10],
    [210,"Wing Attack","Flying",8,800,9,11.25,10],
    [211,"Peck","Flying",10,1000,10,10,10],
    [212,"Lick","Ghost",5,500,6,12,10],
    [213,"Shadow Claw","Ghost",9,700,6,8.571428571428571,12.857142857142858],
    [214,"Vine Whip","Grass",7,600,6,10,11.666666666666668],
    [215,"Razor Leaf","Grass",13,1000,7,7,13],
    [216,"Mud Shot","Ground",5,600,7,11.666666666666668,8.333333333333334],
    [217,"Ice Shard","Ice",12,1200,12,10,10],
    [218,"Frost Breath","Ice",10,900,8,8.88888888888889,11.11111111111111],
    [219,"Quick Attack","Normal",8,800,10,12.5,10],
    [220,"Scratch","Normal",6,500,4,8,12],
    [221,"Tackle","Normal",5,500,5,10,10],
    [222,"Pound","Normal",7,600,6,10,11.666666666666668],
    [223,"Cut","Normal",5,500,5,10,10],
    [224,"Poison Jab","Poison",10,800,7,8.75,12.5],
    [225,"Acid","Poison",9,800,8,10,11.25],
    [226,"Psycho Cut","Psychic",5,600,8,13.333333333333334,8.333333333333334],
    [227,"Rock Throw","Rock",12,900,7,7.777777777777779,13.333333333333334],
    [228,"Metal Claw","Steel",8,700,7,10,11.428571428571429],
    [229,"Bullet Punch","Steel",9,900,10,11.11111111111111,10],
    [230,"Water Gun","Water",5,500,5,10,10],
    [231,"Splash","Water",0,1730,20,11.560693641618498,0],
    [232,"Water Gun Blastoise","Water",10,1000,6,6,10],
    [233,"Mud Slap","Ground",15,1400,12,8.571428571428571,10.714285714285715],
    [234,"Zen Headbutt","Psychic",12,1100,10,9.09090909090909,10.909090909090908],
    [235,"Confusion","Psychic",20,1600,15,9.375,12.5],
    [236,"Poison Sting","Poison",5,600,7,11.666666666666668,8.333333333333334],
    [237,"Bubble","Water",12,1200,14,11.666666666666668,10],
    [238,"Feint Attack","Dark",10,900,9,10,11.11111111111111],
    [239,"Steel Wing","Steel",11,800,6,7.5,13.75],
    [240,"Fire Fang","Fire",11,900,8,8.88888888888889,12.222222222222223],
    [241,"Rock Smash","Fighting",15,1300,10,7.692307692307692,11.538461538461537],
    [242,"Transform","Normal",0,2230,0,0,0],
    [243,"Counter","Fighting",12,900,8,8.88888888888889,13.333333333333334],
    [244,"Powder Snow","Ice",6,1000,15,15,6],
    [249,"Charge Beam","Electric",8,1100,15,13.636363636363637,7.2727272727272725],
    [250,"Volt Switch","Electric",20,2300,25,10.869565217391305,8.695652173913045],
    [253,"Dragon Tail","Dragon",15,1100,9,8.181818181818182,13.636363636363637],
    [255,"Air Slash","Flying",14,1200,10,8.333333333333334,11.666666666666668],
    [260,"Infestation","Bug",10,1100,14,12.727272727272727,9.09090909090909],
    [261,"Struggle Bug","Bug",15,1500,15,10,10],
    [263,"Astonish","Ghost",8,1100,14,12.727272727272727,7.2727272727272725],
    [264,"Hex","Ghost",10,1200,15,12.5,8.333333333333334],
    [266,"Iron Tail","Steel",15,1100,7,6.363636363636363,13.636363636363637],
    [269,"Fire Spin","Fire",14,1100,10,9.09090909090909,12.727272727272727],
    [271,"Bullet Seed","Grass",8,1100,14,12.727272727272727,7.2727272727272725],
    [274,"Extrasensory","Psychic",12,1100,12,10.909090909090908,10.909090909090908],
    [278,"Snarl","Dark",12,1100,12,10.909090909090908,10.909090909090908],
    [281,"Hidden Power","Normal",15,1500,15,10,10],
    [282,"Take Down","Normal",8,1200,10,8.333333333333334,6.666666666666667],
    [283,"Waterfall","Water",16,1200,8,6.666666666666667,13.333333333333334],
    [287,"Yawn","Normal",0,1700,15,8.823529411764707,0],
    [291,"Present","Normal",5,1300,20,15.384615384615383,3.846153846153846],
    [297,"Smack Down","Rock",16,1200,8,6.666666666666667,13.333333333333334],
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
    
# Adapted from the GAME_MASTER_FILE Json Output at:
# https://github.com/pokemongo-dev-contrib/pokemongo-game-master/
# https://raw.githubusercontent.com/pokemongo-dev-contrib/pokemongo-game-master/master/versions/latest/GAME_MASTER.json
CHARGE_MOVE_DATA = [
    # ID    Name    Type    PW  Duration (ms)   Crit%   NRG Cost
    [13,"Wrap","Normal",60,2900,5,33],
    [14,"Hyper Beam","Normal",150,3800,5,100],
    [16,"Dark Pulse","Dark",80,3000,5,50],
    [18,"Sludge","Poison",50,2100,5,33],
    [20,"Vice Grip","Normal",35,1900,5,33],
    [21,"Flame Wheel","Fire",60,2700,5,50],
    [22,"Megahorn","Bug",90,2200,5,100],
    [24,"Flamethrower","Fire",70,2200,5,50],
    [26,"Dig","Ground",100,4700,5,50],
    [28,"Cross Chop","Fighting",50,1500,5,50],
    [30,"Psybeam","Psychic",70,3200,5,50],
    [31,"Earthquake","Ground",120,3600,5,100],
    [32,"Stone Edge","Rock",100,2300,5,100],
    [33,"Ice Punch","Ice",50,1900,5,33],
    [34,"Heart Stamp","Psychic",40,1900,5,33],
    [35,"Discharge","Electric",65,2500,5,33],
    [36,"Flash Cannon","Steel",100,2700,5,100],
    [38,"Drill Peck","Flying",60,2300,5,33],
    [39,"Ice Beam","Ice",90,3300,5,50],
    [40,"Blizzard","Ice",130,3100,5,100],
    [42,"Heat Wave","Fire",95,3000,5,100],
    [45,"Aerial Ace","Flying",55,2400,5,33],
    [46,"Drill Run","Ground",80,2800,5,50],
    [47,"Petal Blizzard","Grass",110,2600,5,100],
    [48,"Mega Drain","Grass",25,2600,5,50],
    [49,"Bug Buzz","Bug",90,3700,5,50],
    [50,"Poison Fang","Poison",35,1700,5,33],
    [51,"Night Slash","Dark",50,2200,5,33],
    [53,"Bubble Beam","Water",45,1900,5,33],
    [54,"Submission","Fighting",60,2200,5,50],
    [56,"Low Sweep","Fighting",40,1900,5,33],
    [57,"Aqua Jet","Water",45,2600,5,33],
    [58,"Aqua Tail","Water",50,1900,5,33],
    [59,"Seed Bomb","Grass",55,2100,5,33],
    [60,"Psyshock","Psychic",65,2700,5,33],
    [62,"Ancient Power","Rock",70,3500,5,33],
    [63,"Rock Tomb","Rock",70,3200,5,50],
    [64,"Rock Slide","Rock",80,2700,5,50],
    [65,"Power Gem","Rock",80,2900,5,50],
    [66,"Shadow Sneak","Ghost",50,2900,5,33],
    [67,"Shadow Punch","Ghost",40,1700,5,33],
    [69,"Ominous Wind","Ghost",50,2300,5,33],
    [70,"Shadow Ball","Ghost",100,3000,5,50],
    [72,"Magnet Bomb","Steel",70,2800,5,33],
    [74,"Iron Head","Steel",60,1900,5,50],
    [75,"Parabolic Charge","Electric",25,2800,5,50],
    [77,"Thunder Punch","Electric",45,1800,5,33],
    [78,"Thunder","Electric",100,2400,5,100],
    [79,"Thunderbolt","Electric",80,2500,5,50],
    [80,"Twister","Dragon",45,2800,5,33],
    [82,"Dragon Pulse","Dragon",90,3600,5,50],
    [83,"Dragon Claw","Dragon",50,1700,5,33],
    [84,"Disarming Voice","Fairy",70,3900,5,33],
    [85,"Draining Kiss","Fairy",60,2600,5,50],
    [86,"Dazzling Gleam","Fairy",100,3500,5,50],
    [87,"Moonblast","Fairy",130,3900,5,100],
    [88,"Play Rough","Fairy",90,2900,5,50],
    [89,"Cross Poison","Poison",40,1500,5,33],
    [90,"Sludge Bomb","Poison",80,2300,5,50],
    [91,"Sludge Wave","Poison",110,3200,5,100],
    [92,"Gunk Shot","Poison",130,3100,5,100],
    [94,"Bone Club","Ground",40,1600,5,33],
    [95,"Bulldoze","Ground",80,3500,5,50],
    [96,"Mud Bomb","Ground",55,2300,5,33],
    [99,"Signal Beam","Bug",75,2900,5,50],
    [100,"X-Scissor","Bug",45,1600,5,33],
    [101,"Flame Charge","Fire",70,3800,5,33],
    [102,"Flame Burst","Fire",70,2600,5,50],
    [103,"Fire Blast","Fire",140,4200,5,100],
    [104,"Brine","Water",60,2300,5,50],
    [105,"Water Pulse","Water",70,3200,5,50],
    [106,"Scald","Water",80,3700,5,50],
    [107,"Hydro Pump","Water",130,3300,5,100],
    [108,"Psychic","Psychic",100,2800,5,100],
    [109,"Psystrike","Psychic",100,4400,5,50],
    [111,"Icy Wind","Ice",60,3300,5,33],
    [114,"Giga Drain","Grass",50,3900,5,100],
    [115,"Fire Punch","Fire",55,2200,5,33],
    [116,"Solar Beam","Grass",180,4900,5,100],
    [117,"Leaf Blade","Grass",70,2400,5,33],
    [118,"Power Whip","Grass",90,2600,5,50],
    [121,"Air Cutter","Flying",60,2700,5,50],
    [122,"Hurricane","Flying",110,2700,5,100],
    [123,"Brick Break","Fighting",40,1600,5,33],
    [125,"Swift","Normal",60,2800,5,50],
    [126,"Horn Attack","Normal",40,1850,5,33],
    [127,"Stomp","Normal",55,1700,5,50],
    [129,"Hyper Fang","Normal",80,2500,5,50],
    [131,"Body Slam","Normal",50,1900,5,33],
    [132,"Rest","Normal",50,1900,5,33],
    [133,"Struggle","Normal",35,2200,5,0],
    [134,"Scald Blastoise","Water",50,4700,5,100],
    [135,"Hydro Pump Blastoise","Water",90,4500,5,100],
    [136,"Wrap Green","Normal",25,2900,5,33],
    [137,"Wrap Pink","Normal",25,2900,5,33],
    [245,"Close Combat","Fighting",100,2300,5,100],
    [246,"Dynamic Punch","Fighting",90,2700,5,50],
    [247,"Focus Blast","Fighting",140,3500,5,100],
    [248,"Aurora Beam","Ice",80,3550,5,50],
    [251,"Wild Charge","Electric",90,2600,5,50],
    [252,"Zap Cannon","Electric",140,3700,5,100],
    [254,"Avalanche","Ice",90,2700,5,50],
    [256,"Brave Bird","Flying",90,2000,5,100],
    [257,"Sky Attack","Flying",80,2000,5,50],
    [258,"Sand Tomb","Ground",80,4000,5,50],
    [259,"Rock Blast","Rock",50,2100,5,33],
    [262,"Silver Wind","Bug",70,3700,5,33],
    [265,"Night Shade","Ghost",60,2600,5,50],
    [267,"Gyro Ball","Steel",80,3300,5,50],
    [268,"Heavy Slam","Steel",70,2100,5,50],
    [270,"Overheat","Fire",160,4000,5,100],
    [272,"Grass Knot","Grass",90,2600,5,50],
    [273,"Energy Ball","Grass",90,3900,5,50],
    [275,"Futuresight","Psychic",120,2700,5,100],
    [276,"Mirror Coat","Psychic",60,2600,5,50],
    [277,"Outrage","Dragon",110,3900,5,50],
    [279,"Crunch","Dark",70,3200,5,33],
    [280,"Foul Play","Dark",70,2000,5,50],
    [284,"Surf","Water",65,1700,5,50],
    [285,"Draco Meteor","Dragon",150,3600,5,100],
    [286,"Doom Desire","Steel",80,1700,5,50],
    [288,"Psycho Boost","Psychic",70,4000,5,50],
    [289,"Origin Pulse","Water",130,1700,5,100],
    [290,"Precipice Blades","Ground",130,1700,5,100],
    [292,"Weather Ball Fire","Fire",60,1600,5,33],
    [293,"Weather Ball Ice","Ice",60,1600,5,33],
    [294,"Weather Ball Rock","Rock",60,1600,5,33],
    [295,"Weather Ball Water","Water",60,1600,5,33],
    [296,"Frenzy Plant","Grass",100,2600,5,50],
    [298,"Blast Burn","Fire",110,3300,5,50],
    [299,"Hydro Cannon","Water",90,1900,5,50],
    [300,"Last Resort","Normal",90,2900,5,50],
]



def _get_charge_move_by_name(name):
    for mv in CHARGE_MOVE_DATA:
        if name == mv[CHARGE_MOVE.Name]:
            return mv
    return None


