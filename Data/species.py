import moves

class Species:
    def __init__(self, name):
        species_data = get_species_data_from_species(name)
        self.Name = species_data[SPECIES_KEYS.Name]
        self.Family = species_data[SPECIES_KEYS.Family]
        self.Id = species_data[SPECIES_KEYS.Id]
        self.HP = species_data[SPECIES_KEYS.HP]
        self.Attack = species_data[SPECIES_KEYS.Attack]
        self.Defense = species_data[SPECIES_KEYS.Defense]
        self.Min_CP = species_data[SPECIES_KEYS.Min_CP]
        self.Max_CP = species_data[SPECIES_KEYS.Max_CP]
        self.Type1 = species_data[SPECIES_KEYS.Type1]
        self.Type2 = species_data[SPECIES_KEYS.Type2]
        self.Evolves_Into = species_data[SPECIES_KEYS.Evolves_Into]
        self.Evolves_From = species_data[SPECIES_KEYS.Evolves_From]
        self.Quick_Moves = species_data[SPECIES_KEYS.Quick_Moves]
        self.Charge_Moves = species_data[SPECIES_KEYS.Charge_Moves]


    @staticmethod
    def _get_species_from_species_name(name):
        spc = Species()


class SPECIES_KEYS:
    Name = 0
    Family = 1
    Id = 2
    HP = 3
    Attack = 4
    Defense = 5
    Min_CP = 6
    Max_CP = 7
    Type1 = 8
    Type2 = 9
    Evolves_Into = 10
    Evolves_From = 11
    Quick_Moves = 12
    Charge_Moves = 13


# Adapted from the spreadsheet
RAW_SPECIES_DATA = [
    # Assumed to be sorted by PKID
    ["Bulbasaur",1,1,90,118,118,764,988,"Grass","Poison",["Ivysaur"],"",["Vine Whip", "Tackle"],["Sludge Bomb", "Seed Bomb", "Power Whip"]],
    ["Ivysaur",1,2,120,151,151,1278,1563,"Grass","Poison",["Venusaur"],"Bulbasaur",["Razor Leaf", "Vine Whip"],["Sludge Bomb", "Solar Beam", "Power Whip"]],
    ["Venusaur",1,3,160,198,198,2216,2586,"Grass","Poison",[""],"Ivysaur",["Razor Leaf", "Vine Whip"],["Sludge Bomb", "Petal Blizzard", "Solar Beam"]],
    ["Charmander",4,4,78,116,96,631,837,"Fire","",["Charmeleon"],"",["Ember", "Scratch"],["Flame Charge", "Flame Burst", "Flamethrower"]],
    ["Charmeleon",4,5,116,158,129,1215,1494,"Fire","",["Charizard"],"Charmander",["Ember", "Fire Fang"],["Fire Punch", "Flame Burst", "Flamethrower"]],
    ["Charizard",4,6,156,223,176,2324,2705,"Fire","Flying",[""],"Charmeleon",["Fire Spin", "Air Slash"],["Fire Blast", "Dragon Claw", "Overheat"]],
    ["Squirtle",7,7,88,94,122,612,814,"Water","",["Wartortle"],"",["Bubble", "Tackle"],["Aqua Jet", "Aqua Tail", "Water Pulse"]],
    ["Wartortle",7,8,118,126,155,1071,1333,"Water","",["Blastoise"],"Squirtle",["Water Gun", "Bite"],["Aqua Jet", "Ice Beam", "Hydro Pump"]],
    ["Blastoise",7,9,158,171,210,1959,2308,"Water","",[""],"Wartortle",["Water Gun", "Bite"],["Flash Cannon", "Ice Beam", "Hydro Pump"]],
    ["Caterpie",10,10,90,55,62,258,395,"Bug","",["Metapod"],"",["Bug Bite", "Tackle"],["Struggle"]],
    ["Metapod",10,11,100,45,94,274,422,"Bug","",["Butterfree"],"Caterpie",["Bug Bite", "Tackle"],["Struggle"]],
    ["Butterfree",10,12,120,167,151,1414,1713,"Bug","Flying",[""],"Metapod",["Struggle Bug", "Confusion"],["Bug Buzz", "Psychic", "Signal Beam"]],
    ["Weedle",13,13,80,63,55,262,400,"Bug","Poison",["Kakuna"],"",["Bug Bite", "Poison Sting"],["Struggle"]],
    ["Kakuna",13,14,90,46,86,254,395,"Bug","Poison",["Beedrill"],"Weedle",["Bug Bite", "Poison Sting"],["Struggle"]],
    ["Beedrill",13,15,130,169,150,1484,1790,"Bug","Poison",[""],"Kakuna",["Infestation", "Poison Jab"],["Sludge Bomb", "Aerial Ace", "X-Scissor"]],
    ["Pidgey",16,16,80,85,76,416,584,"Normal","Flying",["Pidgeotto"],"",["Quick Attack", "Tackle"],["Twister", "Aerial Ace", "Air Cutter"]],
    ["Pidgeotto",16,17,126,117,108,858,1093,"Normal","Flying",["Pidgeot"],"Pidgey",["Wing Attack", "Steel Wing"],["Twister", "Aerial Ace", "Air Cutter"]],
    ["Pidgeot",16,18,166,166,157,1685,2008,"Normal","Flying",[""],"Pidgeotto",["Air Slash", "Steel Wing"],["Hurricane", "Aerial Ace", "Brave Bird"]],
    ["Rattata",19,19,60,103,70,419,592,"Normal","",["Raticate"],"",["Tackle", "Quick Attack"],["Dig", "Hyper Fang", "Body Slam"]],
    ["Raticate",19,20,110,161,144,1274,1560,"Normal","",[""],"Rattata",["Bite", "Quick Attack"],["Dig", "Hyper Fang", "Hyper Beam"]],
    ["Spearow",21,21,80,112,61,492,678,"Normal","Flying",["Fearow"],"",["Peck", "Quick Attack"],["Aerial Ace", "Drill Peck", "Sky Attack"]],
    ["Fearow",21,22,130,182,135,1516,1827,"Normal","Flying",[""],"Spearow",["Peck", "Steel Wing"],["Aerial Ace", "Drill Run", "Sky Attack"]],
    ["Ekans",23,23,70,110,102,584,784,"Poison","",["Arbok"],"",["Poison Sting", "Acid"],["Wrap", "Poison Fang", "Sludge Bomb"]],
    ["Arbok",23,24,120,167,158,1446,1749,"Poison","",[""],"Ekans",["Bite", "Acid"],["Dark Pulse", "Sludge Wave", "Gunk Shot"]],
    ["Pikachu",25,25,70,112,101,592,793,"Electric","",["Raichu"],"Pichu",["Thunder Shock", "Quick Attack"],["Discharge", "Thunderbolt", "Wild Charge"]],
    ["Raichu",25,26,120,193,165,1708,2039,"Electric","",[""],"Pikachu",["Volt Switch", "Spark"],["Brick Break", "Thunder Punch", "Wild Charge"]],
    ["Sandshrew",27,27,100,126,145,954,1203,"Ground","",["Sandslash"],"",["Scratch", "Mud Shot"],["Dig", "Rock Slide", "Sand Tomb"]],
    ["Sandslash",27,28,150,182,202,1992,2344,"Ground","",[""],"Sandshrew",["Metal Claw", "Mud Shot"],["Earthquake", "Rock Tomb", "Bulldoze"]],
    ["Nidoran F",29,29,110,86,94,550,741,"Poison","",["Nidorina"],"",["Bite", "Poison Sting"],["Poison Fang", "Body Slam", "Sludge Bomb"]],
    ["Nidorina",29,30,140,117,126,977,1227,"Poison","",["Nidoqueen"],"Nidoran F",["Bite", "Poison Sting"],["Poison Fang", "Dig", "Sludge Bomb"]],
    ["Nidoqueen",29,31,180,180,174,2003,2354,"Poison","Ground",[""],"Nidorina",["Poison Jab", "Bite"],["Earthquake", "Sludge Wave", "Stone Edge"]],
    ["Nidoran M",32,32,92,105,76,552,744,"Poison","",["Nidorino"],"",["Peck", "Poison Sting"],["Horn Attack", "Body Slam", "Sludge Bomb"]],
    ["Nidorino",32,33,122,137,112,1007,1261,"Poison","",["Nidoking"],"Nidoran M",["Poison Jab", "Poison Sting"],["Horn Attack", "Dig", "Sludge Bomb"]],
    ["Nidoking",32,34,162,204,157,2046,2403,"Poison","Ground",[""],"Nidorino",["Poison Jab", "Iron Tail"],["Earthquake", "Sludge Wave", "Megahorn"]],
    ["Clefairy",35,35,140,107,116,857,1093,"Fairy","",["Clefable"],"Cleffa",["Pound", "Zen Headbutt"],["Disarming Voice", "Body Slam", "Moonblast"]],
    ["Clefable",35,36,190,178,171,2018,2370,"Fairy","",[""],"Clefairy",["Charge Beam", "Zen Headbutt"],["Dazzling Gleam", "Psychic", "Moonblast"]],
    ["Vulpix",37,37,76,96,122,581,779,"Fire","",["Ninetales"],"",["Quick Attack", "Ember"],["Body Slam", "Flamethrower", "Flame Charge"]],
    ["Ninetales",37,38,146,169,204,1834,2173,"Fire","",[""],"Vulpix",["Feint Attack", "Fire Spin"],["Heat Wave", "Overheat", "Solar Beam"]],
    ["Jigglypuff",39,39,230,80,44,506,718,"Normal","Fairy",["Wigglytuff"],"Igglybuff",["Pound", "Feint Attack"],["Disarming Voice", "Gyro Ball", "Dazzling Gleam"]],
    ["Wigglytuff",39,40,280,156,93,1583,1919,"Normal","Fairy",[""],"Jigglypuff",["Pound", "Feint Attack"],["Dazzling Gleam", "Hyper Beam", "Play Rough"]],
    ["Zubat",41,41,80,83,76,407,573,"Poison","Flying",["Golbat"],"",["Quick Attack", "Bite"],["Poison Fang", "Air Cutter", "Swift"]],
    ["Golbat",41,42,150,161,153,1534,1843,"Poison","Flying",["Crobat"],"Zubat",["Wing Attack", "Bite"],["Shadow Ball", "Air Cutter", "Poison Fang"]],
    ["Oddish",43,43,90,131,116,841,1077,"Grass","Poison",["Gloom"],"",["Razor Leaf", "Acid"],["Seed Bomb", "Sludge Bomb", "Moonblast"]],
    ["Gloom",43,44,120,153,139,1242,1523,"Grass","Poison",["Vileplume","Bellossom"],"Oddish",["Razor Leaf", "Acid"],["Petal Blizzard", "Sludge Bomb", "Moonblast"]],
    ["Vileplume",43,45,150,202,170,2029,2384,"Grass","Poison",[""],"Gloom",["Razor Leaf", "Acid"],["Petal Blizzard", "Solar Beam", "Moonblast"]],
    ["Paras",46,46,70,121,99,633,842,"Bug","Grass",["Parasect"],"",["Scratch", "Bug Bite"],["Cross Poison", "X-Scissor", "Seed Bomb"]],
    ["Parasect",46,47,120,165,146,1373,1669,"Bug","Grass",[""],"Paras",["Struggle Bug", "Fury Cutter"],["Cross Poison", "X-Scissor", "Solar Beam"]],
    ["Venonat",48,48,120,100,102,695,909,"Bug","Poison",["Venomoth"],"",["Bug Bite", "Confusion"],["Poison Fang", "Psybeam", "Signal Beam"]],
    ["Venomoth",48,49,140,179,150,1631,1951,"Bug","Poison",[""],"Venonat",["Infestation", "Confusion"],["Silver Wind", "Psychic", "Bug Buzz"]],
    ["Diglett",50,50,20,109,88,287,468,"Ground","",["Dugtrio"],"",["Mud Slap", "Scratch"],["Dig", "Mud Bomb", "Rock Tomb"]],
    ["Dugtrio",50,51,70,167,147,1065,1343,"Ground","",[""],"Diglett",["Sucker Punch", "Mud Slap"],["Earthquake", "Mud Bomb", "Stone Edge"]],
    ["Meowth",52,52,80,92,81,465,642,"Normal","",["Persian"],"",["Scratch", "Bite"],["Night Slash", "Dark Pulse", "Foul Play"]],
    ["Persian",52,53,130,150,139,1268,1550,"Normal","",[""],"Meowth",["Scratch", "Feint Attack"],["Foul Play", "Power Gem", "Play Rough"]],
    ["Psyduck",54,54,100,122,96,751,973,"Water","",["Golduck"],"",["Water Gun", "Zen Headbutt"],["Psybeam", "Aqua Tail", "Cross Chop"]],
    ["Golduck",54,55,160,191,163,1940,2287,"Water","",[""],"Psyduck",["Water Gun", "Confusion"],["Psychic", "Hydro Pump", "Ice Beam"]],
    ["Mankey",56,56,80,148,87,776,1009,"Fighting","",["Primeape"],"",["Karate Chop", "Scratch"],["Cross Chop", "Low Sweep", "Brick Break"]],
    ["Primeape",56,57,130,207,144,1781,2120,"Fighting","",[""],"Mankey",["Low Kick", "Counter"],["Close Combat", "Low Sweep", "Night Slash"]],
    ["Growlithe",58,58,110,136,96,879,1118,"Fire","",["Arcanine"],"",["Ember", "Bite"],["Flame Wheel", "Body Slam", "Flamethrower"]],
    ["Arcanine",58,59,180,227,166,2468,2859,"Fire","",[""],"Growlithe",["Fire Fang", "Snarl"],["Fire Blast", "Wild Charge", "Crunch"]],
    ["Poliwag",60,60,80,101,82,514,700,"Water","",["Poliwhirl"],"",["Bubble", "Mud Shot"],["Bubble Beam", "Mud Bomb", "Body Slam"]],
    ["Poliwhirl",60,61,130,130,130,1063,1322,"Water","",["Poliwrath","Politoed"],"Poliwag",["Bubble", "Mud Shot"],["Water Pulse", "Mud Bomb", "Bubble Beam"]],
    ["Poliwrath",60,62,180,182,187,2100,2459,"Water","Fighting",[""],"Poliwhirl",["Bubble", "Rock Smash"],["Hydro Pump", "Dynamic Punch", "Ice Punch"]],
    ["Abra",63,63,50,195,103,880,1156,"Psychic","",["Kadabra"],"",["Zen Headbutt", "Charge Beam"],["Psyshock", "Signal Beam", "Shadow Ball"]],
    ["Kadabra",63,64,80,232,138,1533,1873,"Psychic","",["Alakazam"],"Abra",["Psycho Cut", "Confusion"],["Psybeam", "Dazzling Gleam", "Shadow Ball"]],
    ["Alakazam",63,65,110,271,194,2490,2907,"Psychic","",[""],"Kadabra",["Psycho Cut", "Confusion"],["Futuresight", "Focus Blast", "Shadow Ball"]],
    ["Machop",66,66,140,137,88,956,1208,"Fighting","",["Machoke"],"",["Rock Smash", "Karate Chop"],["Low Sweep", "Brick Break", "Cross Chop"]],
    ["Machoke",66,67,160,177,130,1605,1923,"Fighting","",["Machamp"],"Machop",["Low Kick", "Karate Chop"],["Submission", "Brick Break", "Dynamic Punch"]],
    ["Machamp",66,68,180,234,162,2513,2909,"Fighting","",[""],"Machoke",["Bullet Punch", "Counter"],["Heavy Slam", "Dynamic Punch", "Close Combat"]],
    ["Bellsprout",69,69,100,139,64,699,923,"Grass","Poison",["Weepinbell"],"",["Vine Whip", "Acid"],["Power Whip", "Sludge Bomb", "Wrap"]],
    ["Weepinbell",69,70,130,172,95,1202,1485,"Grass","Poison",["Victreebel"],"Bellsprout",["Bullet Seed", "Acid"],["Power Whip", "Sludge Bomb", "Seed Bomb"]],
    ["Victreebel",69,71,160,207,138,1934,2285,"Grass","Poison",[""],"Weepinbell",["Razor Leaf", "Acid"],["Leaf Blade", "Sludge Bomb", "Solar Beam"]],
    ["Tentacool",72,72,80,97,182,736,963,"Water","Poison",["Tentacruel"],"",["Bubble", "Poison Sting"],["Bubble Beam", "Water Pulse", "Wrap"]],
    ["Tentacruel",72,73,160,166,237,2033,2390,"Water","Poison",[""],"Tentacool",["Acid", "Poison Jab"],["Hydro Pump", "Sludge Wave", "Blizzard"]],
    ["Geodude",74,74,80,132,163,948,1202,"Rock","Ground",["Graveler"],"",["Rock Throw", "Tackle"],["Rock Slide", "Rock Tomb", "Dig"]],
    ["Graveler",74,75,110,164,196,1514,1828,"Rock","Ground",["Golem"],"Geodude",["Rock Throw", "Mud Slap"],["Dig", "Stone Edge", "Rock Blast"]],
    ["Golem",74,76,160,211,229,2540,2937,"Rock","Ground",[""],"Graveler",["Rock Throw", "Mud Slap"],["Stone Edge", "Rock Blast", "Earthquake"]],
    ["Ponyta",77,77,100,170,132,1228,1513,"Fire","",["Rapidash"],"",["Tackle", "Ember"],["Flame Charge", "Flame Wheel", "Stomp"]],
    ["Rapidash",77,78,130,207,167,1918,2268,"Fire","",[""],"Ponyta",["Low Kick", "Fire Spin"],["Fire Blast", "Drill Run", "Heat Wave"]],
    ["Slowpoke",79,79,180,109,109,960,1212,"Water","Psychic",["Slowbro","Slowking"],"",["Water Gun", "Confusion"],["Water Pulse", "Psyshock", "Psychic"]],
    ["Slowbro",79,80,190,177,194,2137,2499,"Water","Psychic",[""],"Slowpoke",["Water Gun", "Confusion"],["Water Pulse", "Psychic", "Ice Beam"]],
    ["Magnemite",81,81,50,165,128,830,1091,"Electric","Steel",["Magneton"],"",["Spark", "Thunder Shock"],["Discharge", "Magnet Bomb", "Thunderbolt"]],
    ["Magneton",81,82,100,223,182,1892,2253,"Electric","Steel",[""],"Magnemite",["Spark", "Charge Beam"],["Zap Cannon", "Magnet Bomb", "Flash Cannon"]],
    ["Farfetchd",83,83,104,124,118,864,1099,"Normal","Flying",[""],"",["Air Slash", "Fury Cutter"],["Aerial Ace", "Air Cutter", "Leaf Blade"]],
    ["Doduo",84,84,70,158,88,780,1018,"Normal","Flying",["Dodrio"],"",["Peck", "Quick Attack"],["Drill Peck", "Aerial Ace", "Brave Bird"]],
    ["Dodrio",84,85,120,218,145,1808,2154,"Normal","Flying",[""],"Doduo",["Feint Attack", "Steel Wing"],["Drill Peck", "Aerial Ace", "Brave Bird"]],
    ["Seel",86,86,130,85,128,689,905,"Water","",["Dewgong"],"",["Ice Shard", "Lick"],["Aurora Beam", "Icy Wind", "Aqua Tail"]],
    ["Dewgong",86,87,180,139,184,1591,1908,"Water","Ice",[""],"Seel",["Frost Breath", "Iron Tail"],["Aurora Beam", "Water Pulse", "Blizzard"]],
    ["Grimer",88,88,160,135,90,1019,1279,"Poison","",["Muk"],"",["Poison Jab", "Mud Slap"],["Sludge", "Mud Bomb", "Sludge Bomb"]],
    ["Muk",88,89,210,190,184,2349,2728,"Poison","",[""],"Grimer",["Infestation", "Poison Jab"],["Dark Pulse", "Gunk Shot", "Sludge Wave"]],
    ["Shellder",90,90,60,116,168,732,965,"Water","",["Cloyster"],"",["Ice Shard", "Tackle"],["Bubble Beam", "Water Pulse", "Icy Wind"]],
    ["Cloyster",90,91,100,186,323,2102,2492,"Water","Ice",[""],"Shellder",["Frost Breath", "Ice Shard"],["Aurora Beam", "Hydro Pump", "Avalanche"]],
    ["Gastly",92,92,60,186,70,758,1009,"Ghost","Poison",["Haunter"],"",["Lick", "Astonish"],["Night Shade", "Dark Pulse", "Sludge Bomb"]],
    ["Haunter",92,93,90,223,112,1408,1728,"Ghost","Poison",["Gengar"],"Gastly",["Shadow Claw", "Astonish"],["Shadow Punch", "Dark Pulse", "Sludge Bomb"]],
    ["Gengar",92,94,120,261,156,2246,2637,"Ghost","Poison",[""],"Haunter",["Sucker Punch", "Hex"],["Shadow Ball", "Focus Blast", "Sludge Bomb"]],
    ["Onix",95,95,70,85,288,759,1009,"Rock","Ground",["Steelix"],"",["Rock Throw", "Tackle"],["Sand Tomb", "Stone Edge", "Heavy Slam"]],
    ["Drowzee",96,96,120,89,158,770,999,"Psychic","",["Hypno"],"",["Pound", "Confusion"],["Psybeam", "Psyshock", "Psychic"]],
    ["Hypno",96,97,170,144,215,1731,2063,"Psychic","",[""],"Drowzee",["Zen Headbutt", "Confusion"],["Futuresight", "Psychic", "Focus Blast"]],
    ["Krabby",98,98,60,181,156,1101,1396,"Water","",["Kingler"],"",["Bubble", "Mud Shot"],["Vice Grip", "Bubble Beam", "Water Pulse"]],
    ["Kingler",98,99,110,240,214,2316,2713,"Water","",[""],"Krabby",["Bubble", "Metal Claw"],["Vice Grip", "X-Scissor", "Water Pulse"]],
    ["Voltorb",100,100,80,109,114,654,863,"Electric","",["Electrode"],"",["Spark", "Tackle"],["Discharge", "Thunderbolt", "Gyro Ball"]],
    ["Electrode",100,101,120,173,179,1594,1913,"Electric","",[""],"Voltorb",["Spark", "Volt Switch"],["Discharge", "Thunderbolt", "Hyper Beam"]],
    ["Exeggcute",102,102,120,107,140,872,1110,"Grass","Psychic",["Exeggutor"],"",["Confusion", "Bullet Seed"],["Seed Bomb", "Psychic", "Ancient Power"]],
    ["Exeggutor",102,103,190,233,158,2539,2937,"Grass","Psychic",[""],"Exeggcute",["Bullet Seed", "Extrasensory"],["Seed Bomb", "Psychic", "Solar Beam"]],
    ["Cubone",104,104,100,90,165,727,950,"Ground","",["Marowak"],"",["Mud Slap", "Rock Smash"],["Bone Club", "Dig", "Bulldoze"]],
    ["Marowak",104,105,120,144,200,1403,1703,"Ground","",[""],"Cubone",["Mud Slap", "Rock Smash"],["Bone Club", "Dig", "Earthquake"]],
    ["Hitmonlee",236,106,100,224,211,2046,2423,"Fighting","",[""],"Tyrogue",["Low Kick", "Rock Smash"],["Close Combat", "Low Sweep", "Stone Edge"]],
    ["Hitmonchan",236,107,100,193,212,1767,2113,"Fighting","",[""],"Tyrogue",["Bullet Punch", "Counter"],["Fire Punch", "Ice Punch", "Thunder Punch", "Close Combat"]],
    ["Lickitung",108,108,180,108,137,1066,1332,"Normal","",[""],"",["Lick", "Zen Headbutt"],["Hyper Beam", "Stomp", "Power Whip"]],
    ["Koffing",109,109,80,119,164,857,1099,"Poison","",["Weezing"],"",["Tackle", "Infestation"],["Sludge", "Sludge Bomb", "Dark Pulse"]],
    ["Weezing",109,110,130,174,221,1855,2199,"Poison","",[""],"Koffing",["Tackle", "Infestation"],["Sludge Bomb", "Shadow Ball", "Dark Pulse"]],
    ["Rhyhorn",111,111,160,140,157,1395,1691,"Ground","Rock",["Rhydon"],"",["Mud Slap", "Rock Smash"],["Bulldoze", "Horn Attack", "Stomp"]],
    ["Rhydon",111,112,210,222,206,2904,3324,"Ground","Rock",[""],"Rhyhorn",["Mud Slap", "Rock Smash"],["Megahorn", "Earthquake", "Stone Edge"]],
    ["Chansey",113,113,500,60,176,1119,1479,"Normal","",["Blissey"],"",["Pound", "Zen Headbutt"],["Psychic", "Hyper Beam", "Dazzling Gleam"]],
    ["Tangela",114,114,130,183,205,1879,2224,"Grass","",[""],"",["Vine Whip", "Infestation"],["Grass Knot", "Sludge Bomb", "Solar Beam"]],
    ["Kangaskhan",115,115,210,181,165,2119,2481,"Normal","",[""],"",["Mud Slap", "Low Kick"],["Crunch", "Earthquake", "Outrage"]],
    ["Horsea",116,116,60,129,125,702,928,"Water","",["Seadra"],"",["Water Gun", "Bubble"],["Bubble Beam", "Dragon Pulse", "Flash Cannon"]],
    ["Seadra",116,117,110,187,182,1664,1993,"Water","",["Kingdra"],"Horsea",["Water Gun", "Dragon Breath"],["Aurora Beam", "Dragon Pulse", "Hydro Pump"]],
    ["Goldeen",118,118,90,123,115,787,1014,"Water","",["Seaking"],"",["Peck", "Mud Shot"],["Water Pulse", "Horn Attack", "Aqua Tail"]],
    ["Seaking",118,119,160,175,154,1727,2055,"Water","",[""],"Goldeen",["Peck", "Poison Jab"],["Ice Beam", "Water Pulse", "Megahorn"]],
    ["Staryu",120,120,60,137,112,706,933,"Water","",["Starmie"],"",["Tackle", "Water Gun"],["Swift", "Bubble Beam", "Power Gem"]],
    ["Starmie",120,121,120,210,184,1962,2319,"Water","Psychic",[""],"Staryu",["Hidden Power", "Water Gun"],["Hydro Pump", "Power Gem", "Psychic"]],
    ["Mr Mime",122,122,80,192,233,1648,1998,"Psychic","Fairy",[""],"",["Confusion", "Zen Headbutt"],["Psybeam", "Psychic", "Shadow Ball"]],
    ["Scyther",123,123,140,218,170,2115,2481,"Bug","Flying",["Scizor"],"",["Fury Cutter", "Air Slash"],["Night Slash", "X-Scissor", "Aerial Ace"]],
    ["Jynx",124,124,130,223,182,2157,2530,"Ice","Psychic",[""],"Smoochum",["Frost Breath", "Confusion"],["Draining Kiss", "Avalanche", "Psyshock"]],
    ["Electabuzz",125,125,130,198,173,1867,2212,"Electric","",[""],"Elekid",["Thunder Shock", "Low Kick"],["Thunder Punch", "Thunderbolt", "Thunder"]],
    ["Magmar",126,126,130,206,169,1920,2270,"Fire","",[""],"Magby",["Ember", "Karate Chop"],["Fire Blast", "Fire Punch", "Flamethrower"]],
    ["Pinsir",127,127,130,238,197,2395,2790,"Bug","",[""],"",["Rock Smash", "Bug Bite"],["Vice Grip", "X-Scissor", "Close Combat"]],
    ["Tauros",128,128,150,198,197,2141,2505,"Normal","",[""],"",["Tackle", "Zen Headbutt"],["Horn Attack", "Iron Head", "Earthquake"]],
    ["Magikarp",129,129,40,29,102,116,222,"Water","",["Gyarados"],"",["Splash"],["Struggle"]],
    ["Gyarados",129,130,190,237,197,2884,3304,"Water","Flying",[""],"Magikarp",["Bite", "Dragon Tail"],["Hydro Pump", "Crunch", "Outrage"]],
    ["Lapras",131,131,260,165,180,2245,2621,"Water","Ice",[""],"",["Frost Breath", "Water Gun"],["Hydro Pump", "Ice Beam", "Blizzard"]],
    ["Ditto",132,132,96,91,91,535,723,"Normal","",[""],"",["Transform"],["Struggle"]],
    ["Eevee",133,133,110,104,121,754,975,"Normal","",["Vaporeon", "Jolteon", "Flareon","Espeon","Umbreon"],"",["Quick Attack", "Tackle"],["Dig", "Swift"]],
    ["Vaporeon",133,134,260,205,177,2766,3179,"Water","",[""],"Eevee",["Water Gun"],["Water Pulse", "Hydro Pump", "Aqua Tail"]],
    ["Jolteon",133,135,130,232,201,2359,2749,"Electric","",[""],"Eevee",["Thunder Shock", "Volt Switch"],["Discharge", "Thunderbolt", "Thunder"]],
    ["Flareon",133,136,130,246,204,2519,2925,"Fire","",[""],"Eevee",["Ember", "Fire Spin"],["Fire Blast", "Flamethrower", "Overheat"]],
    ["Porygon",137,137,130,153,139,1293,1579,"Normal","",["Porygon2"],"",["Charge Beam", "Hidden Power"],["Solar Beam", "Hyper Beam", "Zap Cannon"]],
    ["Omanyte",138,138,70,155,174,1076,1355,"Rock","Water",["Omastar"],"",["Water Gun", "Mud Shot"],["Ancient Power", "Bubble Beam", "Rock Blast"]],
    ["Omastar",138,139,140,207,227,2321,2704,"Rock","Water",[""],"Omanyte",["Mud Shot", "Water Gun"],["Ancient Power", "Hydro Pump", "Rock Blast"]],
    ["Kabuto",140,140,60,148,162,917,1181,"Rock","Water",["Kabutops"],"",["Scratch", "Mud Shot"],["Ancient Power", "Aqua Jet", "Rock Tomb"]],
    ["Kabutops",140,141,120,220,203,2159,2535,"Rock","Water",[""],"Kabuto",["Mud Shot", "Rock Smash"],["Ancient Power", "Water Pulse", "Stone Edge"]],
    ["Aerodactyl",142,142,160,221,164,2251,2627,"Rock","Flying",[""],"",["Steel Wing", "Bite"],["Ancient Power", "Iron Head", "Hyper Beam"]],
    ["Snorlax",143,143,320,190,190,2946,3379,"Normal","",[""],"",["Zen Headbutt", "Lick"],["Heavy Slam", "Hyper Beam", "Earthquake"]],
    ["Articuno",144,144,180,192,249,2556,2954,"Ice","Flying",[""],"",["Frost Breath"],["Ice Beam", "Icy Wind", "Blizzard"]],
    ["Zapdos",145,145,180,253,188,2927,3354,"Electric","Flying",[""],"",["Charge Beam"],["Zap Cannon", "Thunderbolt", "Thunder"]],
    ["Moltres",146,146,180,251,184,2873,3296,"Fire","Flying",[""],"",["Fire Spin"],["Fire Blast", "Heat Wave", "Overheat"]],
    ["Dratini",147,147,82,119,94,657,866,"Dragon","",["Dragonair"],"",["Dragon Breath", "Iron Tail"],["Wrap", "Twister", "Aqua Tail"]],
    ["Dragonair",147,148,122,163,138,1330,1621,"Dragon","",["Dragonite"],"Dratini",["Dragon Breath", "Iron Tail"],["Wrap", "Aqua Tail", "Dragon Pulse"]],
    ["Dragonite",147,149,182,263,201,3164,3607,"Dragon","Flying",[""],"Dragonair",["Dragon Tail", "Steel Wing"],["Hurricane", "Hyper Beam", "Outrage"]],
    ["Mewtwo",150,150,212,330,200,4274,4794,"Psychic","",[""],"",["Psycho Cut", "Confusion"],["Psychic", "Shadow Ball", "Hyper Beam", "Focus Blast"]],
    ["Mew",151,151,200,210,210,2707,3112,"Psychic","",[""],"",["Pound"],["Blizzard", "Earthquake", "Psychic", "Focus Blast", "Thunder", "Fire Blast", "Solar Beam", "Hyper Beam"]],
    ["Chikorita",152,152,90,92,122,606,807,"","",["Bayleef"],"",["Vine Whip", "Tackle"],["Energy Ball", "Grass Knot", "Body Slam"]],
    ["Bayleef",152,153,120,122,155,1046,1305,"","",["Meganium"],"Chikorita",["Razor Leaf", "Tackle"],["Energy Ball", "Grass Knot", "Ancient Power"]],
    ["Meganium",152,154,160,168,202,1899,2243,"","",[""],"Bayleef",["Razor Leaf", "Vine Whip"],["Petal Blizzard", "Solar Beam", "Earthquake"]],
    ["Cyndaquil",155,155,78,116,96,631,837,"","",["Quilava"],"",["Ember", "Tackle"],["Flame Charge", "Swift", "Flamethrower"]],
    ["Quilava",155,156,116,158,129,1215,1494,"","",["Typhlosion"],"Cyndaquil",["Ember", "Tackle"],["Flame Charge", "Dig", "Flamethrower"]],
    ["Typhlosion",155,157,156,223,176,2324,2705,"","",[""],"Quilava",["Ember", "Shadow Claw"],["Fire Blast", "Overheat", "Solar Beam"]],
    ["Totodile",158,158,100,117,116,792,1019,"","",["Croconaw"],"",["Water Gun", "Scratch"],["Crunch", "Aqua Jet", "Water Pulse"]],
    ["Croconaw",158,159,130,150,151,1321,1610,"","",["Feraligatr"],"Totodile",["Water Gun", "Scratch"],["Crunch", "Ice Punch", "Water Pulse"]],
    ["Feraligatr",158,160,170,205,197,2359,2740,"","",[""],"Croconaw",["Water Gun", "Bite"],["Crunch", "Hydro Pump", "Ice Beam"]],
    ["Sentret",161,161,70,79,77,364,522,"","",["Furret"],"",["Scratch", "Quick Attack"],["Dig", "Brick Break", "Grass Knot"]],
    ["Furret",161,162,170,148,130,1383,1679,"","",[""],"Sentret",["Quick Attack", "Sucker Punch"],["Dig", "Brick Break", "Hyper Beam"]],
    ["Hoothoot",163,163,120,67,101,463,645,"","Flying",["Noctowl"],"",["Feint Attack", "Peck"],["Blizzard"]],
    ["Noctowl",163,164,200,145,179,1725,2055,"","Flying",[""],"Hoothoot",["Wing Attack", "Extrasensory"],["Psychic", "Sky Attack", "Night Shade"]],
    ["Ledyba",165,165,80,72,142,482,668,"","Flying",["Ledian"],"",["Tackle", "Bug Bite"],["Silver Wind", "Swift", "Aerial Ace"]],
    ["Ledian",165,166,110,107,209,1020,1284,"","Flying",[""],"Ledyba",["Struggle Bug", "Bug Bite"],["Bug Buzz", "Silver Wind", "Aerial Ace"]],
    ["Spinarak",167,167,80,105,73,504,690,"","Poison",["Ariados"],"",["Poison Sting", "Bug Bite"],["Night Slash", "Signal Beam", "Cross Poison"]],
    ["Ariados",167,168,140,161,128,1355,1648,"","Poison",[""],"Spinarak",["Poison Sting", "Infestation"],["Shadow Sneak", "Megahorn", "Cross Poison"]],
    ["Crobat",41,169,170,194,178,2122,2484,"","Flying",[""],"Golbat",["Air Slash", "Bite"],["Shadow Ball", "Air Cutter", "Sludge Bomb"]],
    ["Chinchou",170,170,150,106,106,840,1075,"","Electric",["Lanturn"],"",["Bubble", "Spark"],["Water Pulse", "Thunderbolt", "Bubble Beam"]],
    ["Lanturn",170,171,250,146,146,1754,2091,"","Electric",[""],"Chinchou",["Water Gun", "Charge Beam"],["Hydro Pump", "Thunderbolt", "Thunder"]],
    ["Pichu",25,172,40,77,63,243,379,"","",["Pikachu"],"",["Thunder Shock"],["Thunderbolt", "Disarming Voice", "Thunder Punch"]],
    ["Cleffa",35,173,100,75,91,450,625,"","",["Clefairy"],"",["Pound", "Zen Headbutt"],["Grass Knot", "Psyshock", "Signal Beam"]],
    ["Igglybuff",39,174,180,69,34,339,516,"","Fairy",["Jigglypuff"],"",["Pound", "Feint Attack"],["Wild Charge", "Shadow Ball", "Psychic"]],
    ["Togepi",175,175,70,67,116,379,544,"","",["Togetic"],"",["Hidden Power", "Peck"],["Ancient Power", "Psyshock", "Dazzling Gleam"]],
    ["Togetic",175,176,110,139,191,1267,1554,"","Flying",[""],"Togepi",["Extrasensory", "Hidden Power"],["Ancient Power", "Dazzling Gleam", "Aerial Ace"]],
    ["Natu",177,177,80,134,89,711,931,"","Flying",["Xatu"],"",["Peck", "Quick Attack"],["Night Shade", "Psyshock", "Drill Peck"]],
    ["Xatu",177,178,130,192,146,1663,1989,"","Flying",[""],"Natu",["Air Slash", "Feint Attack"],["Ominous Wind", "Futuresight", "Aerial Ace"]],
    ["Mareep",179,179,110,114,82,681,893,"","",["Flaaffy"],"",["Tackle", "Thunder Shock"],["Body Slam", "Thunderbolt", "Discharge"]],
    ["Flaaffy",179,180,140,145,112,1142,1412,"","",["Ampharos"],"Mareep",["Tackle", "Charge Beam"],["Power Gem", "Thunderbolt", "Discharge"]],
    ["Ampharos",179,181,180,211,172,2335,2714,"","",[""],"Flaaffy",["Charge Beam", "Volt Switch"],["Zap Cannon", "Focus Blast", "Thunder"]],
    ["Bellossom",43,182,150,169,189,1789,2123,"","",[""],"Gloom",["Razor Leaf", "Acid"],["Leaf Blade", "Petal Blizzard", "Dazzling Gleam"]],
    ["Marill",183,183,140,37,93,265,423,"","Fairy",["Azumarill"],"",["Tackle", "Bubble"],["Bubble Beam", "Aqua Tail", "Body Slam"]],
    ["Azumarill",183,184,200,112,152,1228,1513,"","Fairy",[""],"Marill",["Rock Smash", "Bubble"],["Play Rough", "Hydro Pump", "Ice Beam"]],
    ["Sudowoodo",185,185,140,167,198,1748,2080,"","",[""],"",["Rock Throw", "Counter"],["Stone Edge", "Earthquake", "Rock Slide"]],
    ["Politoed",60,186,180,174,192,2034,2388,"","",[""],"Poliwhirl",["Mud Shot", "Bubble"],["Hydro Pump", "Blizzard", "Earthquake"]],
    ["Hoppip",187,187,70,67,101,354,512,"","Flying",["Skiploom"],"",["Tackle", "Bullet Seed"],["Grass Knot", "Dazzling Gleam", "Seed Bomb"]],
    ["Skiploom",187,188,110,91,127,676,888,"","Flying",["Jumpluff"],"Hoppip",["Tackle", "Bullet Seed"],["Grass Knot", "Dazzling Gleam", "Energy Ball"]],
    ["Jumpluff",187,189,150,118,197,1275,1564,"","Flying",[""],"Skiploom",["Infestation", "Bullet Seed"],["Energy Ball", "Dazzling Gleam", "Solar Beam"]],
    ["Aipom",190,190,110,136,112,949,1196,"","",[""],"",["Scratch", "Astonish"],["Low Sweep", "Swift", "Aerial Ace"]],
    ["Sunkern",191,191,60,55,55,198,319,"","",["Sunflora"],"",["Razor Leaf", "Cut"],["Energy Ball", "Grass Knot", "Seed Bomb"]],
    ["Sunflora",191,192,150,185,148,1733,2063,"","",[""],"Sunkern",["Razor Leaf", "Bullet Seed"],["Solar Beam", "Petal Blizzard", "Sludge Bomb"]],
    ["Yanma",193,193,130,154,94,1070,1336,"","Flying",[""],"",["Quick Attack", "Wing Attack"],["Ancient Power", "Aerial Ace", "Silver Wind"]],
    ["Wooper",194,194,110,75,75,428,600,"","Ground",["Quagsire"],"",["Water Gun", "Mud Shot"],["Mud Bomb", "Dig", "Body Slam"]],
    ["Quagsire",194,195,190,152,152,1624,1943,"","Ground",[""],"Wooper",["Water Gun", "Mud Shot"],["Sludge Bomb", "Earthquake", "Stone Edge"]],
    ["Espeon",133,196,130,261,194,2607,3022,"","",[""],"Eevee",["Confusion", "Zen Headbutt"],["Psybeam", "Psychic", "Futuresight"]],
    ["Umbreon",133,197,190,126,250,1727,2067,"","",[""],"Eevee",["Feint Attack", "Snarl"],["Dark Pulse", "Foul Play"]],
    ["Murkrow",198,198,120,175,87,1124,1402,"","Flying",[""],"",["Peck", "Feint Attack"],["Drill Peck", "Foul Play", "Dark Pulse"]],
    ["Slowking",79,199,190,177,194,2137,2499,"","Psychic",[""],"Slowpoke",["Water Gun", "Confusion"],["Blizzard", "Psychic", "Fire Blast"]],
    ["Misdreavus",200,200,120,167,167,1487,1794,"","",[""],"",["Astonish", "Hex"],["Shadow Sneak", "Dark Pulse", "Ominous Wind"]],
    ["Unown",201,201,96,136,91,799,1030,"","",[""],"",["Hidden Power"],["Struggle"]],
    ["Wobbuffet",202,202,380,60,106,757,1031,"","",[""],"",["Counter", "Splash"],["Mirror Coat"]],
    ["Girafarig",203,203,140,182,133,1562,1876,"","Psychic",[""],"",["Tackle", "Confusion"],["Psychic", "Thunderbolt", "Mirror Coat"]],
    ["Pineco",204,204,100,108,146,820,1052,"","",["Forretress"],"",["Tackle", "Bug Bite"],["Gyro Ball", "Rock Tomb", "Sand Tomb"]],
    ["Forretress",204,205,150,161,242,1929,2279,"","Steel",[""],"Pineco",["Bug Bite", "Struggle Bug"],["Heavy Slam", "Earthquake", "Rock Tomb"]],
    ["Dunsparce",206,206,200,131,131,1333,1627,"","",[""],"",["Bite", "Astonish"],["Dig", "Rock Slide", "Drill Run"]],
    ["Gligar",207,207,130,143,204,1464,1771,"","Flying",[""],"",["Fury Cutter", "Wing Attack"],["Dig", "Aerial Ace", "Night Slash"]],
    ["Steelix",95,208,150,148,333,2080,2456,"","Ground",[""],"Onix",["Iron Tail", "Dragon Tail"],["Earthquake", "Heavy Slam", "Crunch"]],
    ["Snubbull",209,209,120,137,89,890,1132,"","",["Granbull"],"",["Tackle", "Bite"],["Crunch", "Dazzling Gleam", "Brick Break"]],
    ["Granbull",209,210,180,212,137,2094,2458,"","",[""],"Snubbull",["Bite", "Snarl"],["Crunch", "Play Rough", "Close Combat"]],
    ["Qwilfish",211,211,130,184,148,1605,1924,"","Poison",[""],"",["Poison Sting", "Water Gun"],["Aqua Tail", "Ice Beam", "Sludge Wave"]],
    ["Scizor",123,212,140,236,191,2427,2821,"","Steel",[""],"Scyther",["Bullet Punch", "Fury Cutter"],["X-Scissor", "Iron Head", "Night Slash"]],
    ["Shuckle",213,213,40,17,396,134,302,"","Rock",[""],"",["Struggle Bug", "Rock Throw"],["Rock Blast", "Stone Edge", "Gyro Ball"]],
    ["Heracross",214,214,160,234,189,2559,2959,"","Fighting",[""],"",["Counter", "Struggle Bug"],["Megahorn", "Close Combat", "Earthquake"]],
    ["Sneasel",215,215,110,189,157,1562,1881,"","Ice",[""],"",["Ice Shard", "Feint Attack"],["Avalanche", "Ice Punch", "Foul Play"]],
    ["Teddiursa",216,216,120,142,93,943,1192,"","",["Ursaring"],"",["Scratch", "Lick"],["Cross Chop", "Crunch", "Play Rough"]],
    ["Ursaring",216,217,180,236,144,2390,2780,"","",[""],"Teddiursa",["Metal Claw", "Counter"],["Close Combat", "Hyper Beam", "Play Rough"]],
    ["Slugma",218,218,80,118,71,559,756,"","",["Magcargo"],"",["Ember", "Rock Throw"],["Flame Burst", "Flame Charge", "Rock Slide"]],
    ["Magcargo",218,219,100,139,209,1264,1554,"","Rock",[""],"Slugma",["Ember", "Rock Throw"],["Heat Wave", "Overheat", "Stone Edge"]],
    ["Swinub",220,220,100,90,74,487,668,"","Ground",["Piloswine"],"",["Tackle", "Powder Snow"],["Icy Wind", "Body Slam", "Rock Slide"]],
    ["Piloswine",220,221,200,181,147,1952,2300,"","Ground",[""],"Swinub",["Ice Shard", "Powder Snow"],["Avalanche", "Bulldoze", "Stone Edge"]],
    ["Corsola",222,222,110,118,156,972,1223,"","Rock",[""],"",["Tackle", "Bubble"],["Rock Blast", "Power Gem", "Bubble Beam"]],
    ["Remoraid",223,223,70,127,69,555,754,"","",["Octillery"],"",["Water Gun", "Mud Shot"],["Aurora Beam", "Water Pulse", "Rock Blast"]],
    ["Octillery",223,224,150,197,141,1802,2139,"","",[""],"Remoraid",["Water Gun", "Mud Shot"],["Gunk Shot", "Water Pulse", "Aurora Beam"]],
    ["Delibird",225,225,90,128,90,724,944,"","Flying",[""],"",["Ice Shard", "Quick Attack"],["Ice Punch", "Icy Wind", "Aerial Ace"]],
    ["Mantine",226,226,130,148,260,1711,2047,"","Flying",[""],"",["Bubble", "Wing Attack"],["Water Pulse", "Ice Beam", "Aerial Ace"]],
    ["Skarmory",227,227,130,148,260,1711,2047,"","Flying",[""],"",["Steel Wing", "Air Slash"],["Brave Bird", "Sky Attack", "Flash Cannon"]],
    ["Houndour",228,228,90,152,93,874,1118,"","Fire",["Houndoom"],"",["Feint Attack", "Ember"],["Crunch", "Flamethrower", "Dark Pulse"]],
    ["Houndoom",228,229,150,224,159,2176,2547,"","Fire",[""],"Houndour",["Snarl", "Fire Fang"],["Crunch", "Fire Blast", "Foul Play"]],
    ["Kingdra",116,230,150,194,194,2081,2441,"","Dragon",[""],"Seadra",["Water Gun", "Dragon Breath"],["Hydro Pump", "Blizzard", "Outrage"]],
    ["Phanpy",231,231,180,107,107,934,1183,"","",["Donphan"],"",["Tackle", "Rock Smash"],["Bulldoze", "Rock Slide", "Body Slam"]],
    ["Donphan",231,232,180,214,214,2641,3043,"","",[""],"Phanpy",["Tackle", "Counter"],["Earthquake", "Heavy Slam", "Play Rough"]],
    ["Porygon2",137,233,170,198,183,2196,2564,"","",[""],"Porygon",["Hidden Power", "Charge Beam"],["Solar Beam", "Hyper Beam", "Zap Cannon"]],
    ["Stantler",234,234,146,192,132,1676,2003,"","",[""],"",["Tackle", "Zen Headbutt"],["Stomp", "Wild Charge", "Megahorn"]],
    ["Smeargle",235,235,110,40,88,247,392,"","",[""],"",["Tackle"],["Struggle"]],
    ["Tyrogue",236,236,70,64,64,269,407,"","",["Hitmonchan","Hitmonlee","Hitmontop"],"",["Rock Smash", "Tackle"],["Brick Break", "Rock Slide", "Low Sweep"]],
    ["Hitmontop",236,237,100,173,214,1591,1919,"","",[""],"Tyrogue",["Rock Smash", "Counter"],["Close Combat", "Gyro Ball", "Stone Edge"]],
    ["Smoochum",124,238,90,153,116,983,1239,"","Psychic",["Jynx"],"",["Powder Snow", "Pound"],["Ice Beam", "Ice Punch", "Psyshock"]],
    ["Elekid",125,239,90,135,110,844,1080,"","",["Electabuzz"],"",["Thunder Shock", "Low Kick"],["Thunder Punch", "Brick Break", "Discharge"]],
    ["Magby",126,240,90,151,108,936,1186,"","",["Magmar"],"",["Ember", "Karate Chop"],["Brick Break", "Fire Punch", "Flame Burst"]],
    ["Miltank",241,241,190,157,211,1977,2328,"","",[""],"",["Tackle", "Zen Headbutt"],["Stomp", "Body Slam", "Gyro Ball"]],
    ["Blissey",113,242,510,129,229,2773,3241,"","",[""],"Chansey",["Pound", "Zen Headbutt"],["Psychic", "Hyper Beam", "Dazzling Gleam"]],
    ["Raikou",243,243,180,241,210,2947,3373,"","",[""],"",["Thunder Shock", "Volt Switch"],["Thunder", "Thunderbolt", "Wild Charge"]],
    ["Entei",244,244,230,235,176,2974,3401,"","",[""],"",["Fire Spin", "Fire Fang"],["Flamethrower", "Fire Blast", "Overheat"]],
    ["Suicune",245,245,200,180,235,2454,2843,"","",[""],"",["Extrasensory", "Snarl"],["Hydro Pump", "Bubble Beam", "Water Pulse"]],
    ["Larvitar",246,246,100,115,93,697,911,"","Ground",["Pupitar"],"",["Bite", "Rock Smash"],["Stomp", "Crunch", "Ancient Power"]],
    ["Pupitar",246,247,140,155,133,1330,1619,"","Ground",["Tyranitar"],"Larvitar",["Bite", "Rock Smash"],["Dig", "Crunch", "Ancient Power"]],
    ["Tyranitar",246,248,200,251,212,3251,3696,"","Dark",[""],"Pupitar",["Bite", "Iron Tail"],["Fire Blast", "Crunch", "Stone Edge"]],
    ["Lugia",249,249,212,193,323,3176,3624,"","Flying",[""],"",["Extrasensory", "Dragon Tail"],["Sky Attack", "Hydro Pump", "Futuresight"]],
    ["Ho-oh",250,250,212,263,301,4179,4683,"","Flying",[""],"",["Extrasensory", "Steel Wing"],["Brave Bird", "Fire Blast", "Solar Beam"]],
    ["Celebi",251,251,200,210,210,2707,3112,"","Grass",[""],"",["Confusion", "Charge Beam"],["Hyper Beam", "Psychic", "Dazzling Gleam"]],
]


def __VALIDATE_POKEMON_MOVES():
    #print("Validating pokemon moves...")
    for species in RAW_SPECIES_DATA:
        for qm in species[SPECIES_KEYS.Quick_Moves]:
            if moves._get_basic_move_by_name(qm) is None:
                print("Invalid move "+qm+" for PKMN "+species[SPECIES_KEYS.Name])
        for cm in species[SPECIES_KEYS.Charge_Moves]:
            if moves._get_charge_move_by_name(cm) is None:
                print("Invalid move "+cm+" for PKMN "+species[SPECIES_KEYS.Name])
__VALIDATE_POKEMON_MOVES()


def get_id_from_species(name):
    for species in RAW_SPECIES_DATA:
            if name.lower() == species[SPECIES_KEYS.Name].lower():
                return int(species[SPECIES_KEYS.Id])
    return -1


def get_species_data_from_species(name):
    return RAW_SPECIES_DATA[get_id_from_species(name)-1]

